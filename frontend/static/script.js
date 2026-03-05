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
const analyzeBtn = document.getElementById("analyze-btn"); // 👈 IMPORTANTE

let backendData = null;
let currentMap = null;

const preview = document.createElement("img");
preview.style.maxWidth = "100%";
preview.style.marginTop = "10px";

const message = document.createElement("div");
message.style.marginTop = "10px";
message.style.fontWeight = "bold";

uploadBox.appendChild(preview);
uploadBox.appendChild(message);


// 🔒 EL BOTÓN EMPIEZA DESACTIVADO
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

        // ✅ ACTIVAR BOTÓN
        if (analyzeBtn) {
            analyzeBtn.disabled = false;
            analyzeBtn.style.opacity = "1";
            analyzeBtn.style.cursor = "pointer";
        }

    } else {

        // ❌ DESACTIVAR SI NO HAY IMAGEN
        if (analyzeBtn) {
            analyzeBtn.disabled = true;
            analyzeBtn.style.opacity = "0.5";
            analyzeBtn.style.cursor = "not-allowed";
        }

    }

});
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

function formatDate(dateString){
    return new Date(dateString).toLocaleString("es-ES");
}

function drawMap(data, maxDistance){

    if(currentMap){
        currentMap.remove();
    }

    currentMap = L.map("map").setView(
        [data.reporte_usuario.latitud, data.reporte_usuario.longitud],
        13
    );

    L.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png", {
        maxZoom: 19,
        attribution: "© OpenStreetMap"
    }).addTo(currentMap);

    const blueIcon = new L.Icon({
        iconUrl: "https://maps.google.com/mapfiles/ms/icons/blue-dot.png",
        iconSize: [32,32]
    });

    const redIcon = new L.Icon({
        iconUrl: "https://maps.google.com/mapfiles/ms/icons/red-dot.png",
        iconSize: [32,32]
    });

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

    const cercanos = data.protegidos_similares.filter(
        p => p.distancia_km <= maxDistance
    );

    cercanos.forEach(pet => {

        L.marker(
            [pet.latitud, pet.longitud],
            {icon: redIcon}
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

form.addEventListener("submit", function(e){

    e.preventDefault();

    const file = fileInput.files[0];
    if(!file){
        message.textContent = "Selecciona una imagen";
        message.style.color = "red";
        return;
    }

    message.textContent = "Solicitando ubicación...";

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

            message.textContent = "Análisis completado ✅";
            message.style.color = "green";

        }catch(err){

            message.textContent = "Error al procesar";
            message.style.color = "red";

        }

    }, function(){

        message.textContent = "No se pudo obtener ubicación";
        message.style.color = "red";

    });

});

document.querySelectorAll(".distance-filter button").forEach(btn => {

    btn.addEventListener("click", function(){

        document.querySelectorAll(".distance-filter button")
        .forEach(b => b.classList.remove("active"));

        this.classList.add("active");

        if(!backendData) return;

        drawMap(backendData, parseInt(this.dataset.km));

    });

});

});