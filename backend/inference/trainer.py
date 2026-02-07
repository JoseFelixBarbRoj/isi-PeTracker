from pathlib import Path

from tqdm import tqdm

from matplotlib import pyplot as plt
import torch
from torch import nn
import numpy as np

class Trainer:
    def __init__(self, 
                 epochs,
                 model: nn.Module,
                 model_name: str,
                 train_dataloader: torch.utils.data.DataLoader,
                 val_dataloader: torch.utils.data.DataLoader,
                 optimizer: torch.optim.Optimizer,
                 output_path: str | Path,
                 loss_fn,
                 acc_fn,
                 device):
        self.device = device
        self.epochs = epochs
        self.model = model.to(device)
        self.model_name = model_name
        self.train_dataloader = train_dataloader
        self.val_dataloader = val_dataloader
        self.optimizer = optimizer
        self.output_path = Path(output_path) / self.model_name
        self.loss_fn = loss_fn
        self.acc_fn = acc_fn
        plt.style.use('ggplot')
        self.output_path.mkdir(exist_ok=True, parents=True)

    def train_one_epoch(self, dataloader: torch.utils.data.DataLoader):
        epoch_loss = 0
        epoch_acc = 0
        
        self.model.train()
        for images, labels in dataloader:
            self.optimizer.zero_grad()
            logits = self.model(images.to(self.device))
            loss = self.loss_fn(logits, labels.to(self.device))
            loss.backward()
            self.optimizer.step()
            acc = self.acc_fn(logits.softmax(dim=1).argmax(dim=1).cpu(), labels)
    
            epoch_loss += loss.item()
            epoch_acc += acc

        return epoch_loss / len(dataloader), epoch_acc / len(dataloader)
 
    def val_one_epoch(self, dataloader: torch.utils.data.DataLoader):
        epoch_loss = 0
        epoch_acc = 0

        self.model.eval()
        with torch.inference_mode():
            for images, labels in dataloader:
                logits = self.model(images.to(self.device))
                loss = self.loss_fn(logits, labels.to(self.device))
                acc = self.acc_fn(logits.softmax(dim=1).argmax(dim=1).cpu(), labels)
        
                epoch_loss += loss.item()
                epoch_acc += acc

        return epoch_loss / len(dataloader), epoch_acc / len(dataloader)
    
    def train(self):
        train_loss_list = []
        val_loss_list = []
        train_acc_list = []
        val_acc_list = []
        epochs = []
        best_val = np.inf

        for epoch in (pbar := tqdm(range(self.epochs))):
            train_loss, train_acc = self.train_one_epoch(dataloader=self.train_dataloader)
            train_loss_list.append(train_loss)
            train_acc_list.append(train_acc)

            val_loss, val_acc = self.val_one_epoch(dataloader=self.val_dataloader)
            val_loss_list.append(val_loss)
            val_acc_list.append(val_acc)
            pbar.set_description(f'[TRAINER] Training model [train_loss={train_loss:.4f}, train_acc={train_acc:.4f}] [val_loss={val_loss:.4f}, val_acc={val_acc:.4f}]')
            
            epochs.append(epoch)

            plt.figure(figsize=(10,7))
            plt.title('Training and validation loss curve')
            plt.plot(epochs, train_loss_list, label='Training', marker='o', markevery=[-1], color='red')
            plt.plot(epochs, val_loss_list, label='Validation', marker='o', markevery=[-1], color='blue')
            plt.xlabel('Epoch')
            plt.ylabel('Loss')
            plt.legend()
            plt.tight_layout()
            plt.savefig(self.output_path / 'loss_curve.png')
            plt.close()

            plt.figure(figsize=(10,7))
            plt.title('Training and validation accuracy curve')
            plt.plot(epochs, train_acc_list, label='Training', marker='o', markevery=[-1], color='red')
            plt.plot(epochs, val_acc_list, label='Validation', marker='o', markevery=[-1], color='blue')
            plt.xlabel('Epoch')
            plt.ylabel('Accuracy')
            plt.legend()
            plt.tight_layout()
            plt.savefig(self.output_path / 'acc_curve.png')
            plt.close()

            if val_loss < best_val:
                torch.save(self.model.state_dict(), self.output_path / 'best.pth')
                best_val = val_loss