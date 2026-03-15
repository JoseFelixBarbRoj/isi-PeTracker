document.addEventListener("DOMContentLoaded", function () {

    // ===== PEDIR PERMISO DE NOTIFICACIONES =====
    if ("Notification" in window) {

        if (Notification.permission === "default") {
            Notification.requestPermission().then(permission => {
                console.log("Permiso de notificaciones:", permission);
            });
        }

    } else {
        console.log("Este navegador no soporta notificaciones.");
    }

const uploadBox = document.getElementById("upload-box");
const fileInput = document.getElementById("pet-photo");
const form = document.getElementById("upload-form");
const analyzeBtn = document.getElementById("analyze-btn");

let backendData = null;
let currentMap = null;

const preview = document.createElement("img");
preview.style.maxWidth = "100%";
preview.style.marginTop = "10px";

const message = document.createElement("div");
message.style.marginTop = "10px";
message.style.fontWeight = "bold";

// spinner de huella
const spinner = document.createElement("span");
spinner.className = "paw-spinner";
spinner.textContent = "🐾";

// texto del mensaje
const messageText = document.createElement("span");

message.appendChild(spinner);
message.appendChild(messageText);

uploadBox.appendChild(preview);
uploadBox.appendChild(message);


// 🔒 BOTÓN DESACTIVADO AL INICIO
if (analyzeBtn) {
    analyzeBtn.disabled = true;
    analyzeBtn.style.opacity = "0.5";
    analyzeBtn.style.cursor = "not-allowed";
}


// CLICK EN EL CUADRO
uploadBox.addEventListener("click", () => fileInput.click());


// PREVIEW AL SELECCIONAR
fileInput.addEventListener("change", () => {

    const file = fileInput.files[0];

    if (file) {

        const reader = new FileReader();
        reader.onload = e => preview.src = e.target.result;
        reader.readAsDataURL(file);

        if (analyzeBtn) {
            analyzeBtn.disabled = false;
            analyzeBtn.style.opacity = "1";
            analyzeBtn.style.cursor = "pointer";
        }

    } else {

        if (analyzeBtn) {
            analyzeBtn.disabled = true;
            analyzeBtn.style.opacity = "0.5";
            analyzeBtn.style.cursor = "not-allowed";
        }

    }

});


// ===== DRAG & DROP =====

uploadBox.addEventListener("dragover", e => {
    e.preventDefault();
    uploadBox.style.border = "2px solid #007bff";
});

uploadBox.addEventListener("dragleave", () => {
    uploadBox.style.border = "2px dashed #ccc";
});

uploadBox.addEventListener("drop", e => {
    e.preventDefault();
    uploadBox.style.border = "2px dashed #ccc";
    fileInput.files = e.dataTransfer.files;
    fileInput.dispatchEvent(new Event("change"));
});


// ===== FORMATEAR FECHA =====

function formatDate(dateString){
    return new Date(dateString).toLocaleString("es-ES");
}


// ===== DIBUJAR MAPA =====

function drawMap(data, maxDistance = 50){

    if(currentMap){
        currentMap.remove();
    }

    currentMap = L.map("map").setView(
        [data.reporte_usuario.latitud, data.reporte_usuario.longitud],
        8
    );

    L.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png", {
        maxZoom: 19,
        attribution: "© OpenStreetMap"
    }).addTo(currentMap);


    const blueIcon = new L.Icon({
        iconUrl: "https://maps.google.com/mapfiles/ms/icons/blue-dot.png",
        iconSize: [32,32]
    });

    const greenIcon = new L.Icon({
        iconUrl: "https://maps.google.com/mapfiles/ms/icons/green-dot.png",
        iconSize: [32,32]
    });


    // ===== TU MASCOTA =====
    
    L.marker(
        [data.reporte_usuario.latitud, data.reporte_usuario.longitud],
        {icon: blueIcon}
    ).addTo(currentMap)
     .bindPopup(`
        <b>🐾 Tu mascota</b><br>
        Raza: ${data.reporte_usuario.raza}<br>
        Usuario: ${data.reporte_usuario.username}<br>
        Fecha: ${formatDate(data.reporte_usuario.fecha)}<br>
        <img src="/${data.reporte_usuario.path_imagen}" width="180">
     `);


    // ===== PROTECTORAS CERCANAS =====

    const cercanos = data.protegidos_similares.filter(
        p => !maxDistance || !p.distancia_km || p.distancia_km <= maxDistance
    );

    cercanos.forEach(pet => {

        L.marker(
            [pet.latitud, pet.longitud],
            {icon: greenIcon}
        ).addTo(currentMap)
         .bindPopup(`
            <b>🏥 Protectora</b><br>
            Raza: ${pet.raza}<br>
            Protectora: ${pet.protectora}<br>
            Distancia: ${pet.distancia_km.toFixed(2)} km<br>
            Fecha: ${formatDate(pet.timestamp)}<br>
            <img src="/${pet.path_imagen}" width="180">
         `);

    });

}


// ===== SUBMIT DEL FORMULARIO =====

form.addEventListener("submit", function(e){

    e.preventDefault();

    const file = fileInput.files[0];

    if(!file){
        spinner.style.display = "none";
        message.textContent = "Selecciona una imagen";
        message.style.color = "red";
        return;
    }

    spinner.style.display = "inline-block";
    messageText.textContent = "📍 Obteniendo ubicación...";
    message.style.color = "black";

    if(!navigator.geolocation){
        message.textContent = "Geolocalización no soportada";
        return;
    }

    navigator.geolocation.getCurrentPosition(async function(position){

        const formData = new FormData();
        formData.append("imagen", file);
        formData.append("latitud", position.coords.latitude);
        formData.append("longitud", position.coords.longitude);

        try{

            const response = await fetch("/predict", {
                method: "POST",
                body: formData
            });

            if(!response.ok) throw new Error("Error servidor");

            const data = await response.json();
            backendData = data;

            drawMap(data, 50);

            spinner.style.display = "none";
            message.textContent = "Análisis completado ✅";
            message.style.color = "green";

        }catch(err){
            spinner.style.display = "none";
            message.textContent = "Error al procesar mapa o modelo";
            message.style.color = "red";

        }

    }, function(){
        spinner.style.display = "none";
        message.textContent = "No se pudo obtener ubicación";
        message.style.color = "red";

    });

});


// ===== FILTROS DE DISTANCIA =====

document.querySelectorAll(".distance-filter button").forEach(btn => {

    btn.addEventListener("click", function(){

        document.querySelectorAll(".distance-filter button")
        .forEach(b => b.classList.remove("active"));

        this.classList.add("active");

        if(!backendData) return;

        const km = this.dataset.km === "all"
            ? Infinity
            : parseInt(this.dataset.km);

        drawMap(backendData, km);

    });

});

});