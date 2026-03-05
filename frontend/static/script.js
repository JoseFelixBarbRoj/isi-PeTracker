document.addEventListener("DOMContentLoaded", function () {

    const uploadBox = document.getElementById("upload-box");
    const fileInput = document.getElementById("pet-photo");
    const form = document.getElementById("upload-form");
    // open street map
    // Preview
    const preview = document.createElement("img");
    preview.style.maxWidth = "100%";
    preview.style.marginTop = "10px";

    const message = document.createElement("div");
    message.style.marginTop = "10px";
    message.style.fontWeight = "bold";

    uploadBox.appendChild(preview);
    uploadBox.appendChild(message);

    // CLICK EN EL CUADRO
    uploadBox.addEventListener("click", function () {
        fileInput.click();
    });

    // PREVIEW AL SELECCIONAR
    fileInput.addEventListener("change", function () {
        handleFile(fileInput.files[0]);
    });

    function handleFile(file) {
        if (!file) return;

        const reader = new FileReader();
        reader.onload = function (e) {
            preview.src = e.target.result;
        };
        reader.readAsDataURL(file);
    }

    // DRAG & DROP
    uploadBox.addEventListener("dragover", function (e) {
        e.preventDefault();
        uploadBox.style.border = "2px solid #007bff";
    });

    uploadBox.addEventListener("dragleave", function () {
        uploadBox.style.border = "2px dashed #ccc";
    });

    uploadBox.addEventListener("drop", function (e) {
        e.preventDefault();
        uploadBox.style.border = "2px dashed #ccc";

        const file = e.dataTransfer.files[0];
        fileInput.files = e.dataTransfer.files;
        handleFile(file);
    });

    form.addEventListener("submit", function (e) {
    e.preventDefault();

    const file = fileInput.files[0];

    if (!file) {
        message.textContent = "Selecciona una imagen";
        message.style.color = "red";
        return;
    }

    message.textContent = "Solicitando ubicación...";
    message.style.color = "black";

    // Pedir ubicación al navegador
    navigator.geolocation.getCurrentPosition(async function (position) {

        const latitude = position.coords.latitude;
        const longitude = position.coords.longitude;

        message.textContent = "Procesando con IA...";
        
        const formData = new FormData();
        formData.append("imagen", file);
        formData.append("latitud", latitude);
        formData.append("longitud", longitude);

        try {
    const response = await fetch("/predict", {
        method: "POST",
        body: formData
    });

    if (!response.ok) throw new Error("Error en el servidor");

    const data = await response.json();
    console.log("Respuesta del backend:", data);

    // === LIMPIAR MAPA ANTERIOR SI EXISTE ===
    if (window.mapInstance) {
        window.mapInstance.remove();
    }

    // === INICIALIZAR LEAFLET CENTRADO EN EL USUARIO ===
    window.mapInstance = L.map('map').setView(
        [data.reporte_usuario.latitud, data.reporte_usuario.longitud],
        13
    );

    // Añadir tiles de OpenStreetMap
    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        maxZoom: 19,
        attribution: '© OpenStreetMap'
    }).addTo(window.mapInstance);

    // === MARCADOR DE LA MASCOTA DEL USUARIO ===
    const userMarker = L.marker([data.reporte_usuario.latitud, data.reporte_usuario.longitud])
        .addTo(window.mapInstance)
        .bindPopup(`<b>Tu mascota perdida</b><br>${data.reporte_usuario.raza}`)
        .openPopup();

    // === MARCADORES DE MASCOTAS PROTEGIDAS SIMILARES ===
    if (data.protegidos_similares.length > 0) {
        data.protegidos_similares.forEach(pet => {
            L.marker([pet.latitud, pet.longitud])
                .addTo(window.mapInstance)
                .bindPopup(`<b>${pet.raza}</b><br>${pet.protectora}`);
        });
    } else {
        console.log("No hay mascotas similares cerca para mostrar en el mapa.");
    }

    // === CONFIRMACIÓN VISUAL ===
    message.textContent = "Análisis completado ✅";
    message.style.color = "green";

} catch (error) {
    console.error("Error al procesar la imagen:", error);
    message.textContent = "Error al procesar la imagen";
    message.style.color = "red";
}

    }, function (error) {
        message.textContent = "No se pudo obtener la ubicación";
        message.style.color = "red";
    });

});

});