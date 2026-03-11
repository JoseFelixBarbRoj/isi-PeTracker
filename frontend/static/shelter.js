function toggleChecklist(){
    const list = document.getElementById("checklist");
    list.style.display = list.style.display === "none" ? "block" : "none";
}

document.addEventListener("DOMContentLoaded", function(){
    const uploadBox = document.getElementById("upload-box");
    const fileInput = document.getElementById("pet-photo");
    const analyzeBtn = document.getElementById("analyze-btn");
    const message = document.getElementById("message");
    const blueIcon = new L.Icon({ iconUrl:"https://maps.google.com/mapfiles/ms/icons/blue-dot.png", iconSize:[32,32] });
    const orangeIcon = new L.Icon({ iconUrl:"https://maps.google.com/mapfiles/ms/icons/orange-dot.png", iconSize:[32,32] });
    const greenIcon = new L.Icon({ iconUrl:"https://maps.google.com/mapfiles/ms/icons/green-dot.png", iconSize:[32,32] });

    const dogIcon = new L.Icon({
        iconUrl: "https://cdn-icons-png.flaticon.com/512/616/616408.png",
        iconSize: [32,32]
    });

    const catIcon = new L.Icon({
        iconUrl: "https://cdn-icons-png.flaticon.com/512/616/616430.png",
        iconSize: [32,32]
    });


    const razas = {

        Perro: [
            "bulldog",
            "boxer",
            "spaniel",
            "beagle",
            "poodle",
            "pomeranian",
            "retriever",
            "dachshund",
            "labrador",
            "husky",
            "doberman",
            "chihuahua"
        ],

        Gato: [
            "ragdoll",
            "siamese",
            "maine_coon",
            "persian",
            "bengal",
            "british_shorthair"
        ]

    };


    let backendData = null;
    let currentMap = null;
    let currentSpecies = "all";

    const preview = document.createElement("img");
    preview.style.maxWidth = "100%";
    preview.style.marginTop = "10px";
    uploadBox.appendChild(preview);

    const distanceButtons = document.querySelectorAll(".distance-filter button");

    distanceButtons.forEach(btn => {
        btn.disabled = true;
        btn.style.opacity = 0.4;
        btn.style.cursor = "not-allowed";
    });

    analyzeBtn.disabled = true;
    analyzeBtn.style.opacity = 0.5;
    analyzeBtn.style.cursor = "not-allowed";

    // Drag & Drop
    uploadBox.addEventListener("click", () => fileInput.click());
    fileInput.addEventListener("change", () => handleFile(fileInput.files[0]));
    uploadBox.addEventListener("dragover", e => { e.preventDefault(); uploadBox.style.border="2px solid #007bff"; });
    uploadBox.addEventListener("dragleave", () => uploadBox.style.border="2px dashed #ccc");
    uploadBox.addEventListener("drop", e => {
        e.preventDefault();
        uploadBox.style.border="2px dashed #ccc";
        fileInput.files = e.dataTransfer.files;
        handleFile(fileInput.files[0]);
    });

    function handleFile(file){
        if(!file) return;
        const reader = new FileReader();
        reader.onload = e => preview.src = e.target.result;
        reader.readAsDataURL(file);
        analyzeBtn.disabled = false;
        analyzeBtn.style.opacity = 1;
        analyzeBtn.style.cursor = "pointer";
    }

    function drawMap(data, maxDistance = Infinity) {
        if(currentMap) currentMap.remove();

        currentMap = L.map("map").setView(
            [data.reporte_actual.latitud, data.reporte_actual.longitud],
            8
        );

        L.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png", {
            maxZoom: 19,
            attribution: "© OpenStreetMap"
        }).addTo(currentMap);

        // ==== ICONOS ====
        const icons = {
            clinic: new L.Icon({ iconUrl:"https://maps.google.com/mapfiles/ms/icons/blue-dot.png", iconSize:[32,32] }),

            lostDog: new L.Icon({ iconUrl:"https://cdn-icons-png.flaticon.com/512/616/616408.png", iconSize:[32,32], className:"orange" }),
            lostCat: new L.Icon({ iconUrl:"https://cdn-icons-png.flaticon.com/512/616/616430.png", iconSize:[32,32], className:"orange" }),

            shelterDog: new L.Icon({ iconUrl:"https://cdn-icons-png.flaticon.com/512/616/616408.png", iconSize:[32,32], className:"green" }),
            shelterCat: new L.Icon({ iconUrl:"https://cdn-icons-png.flaticon.com/512/616/616430.png", iconSize:[32,32], className:"green" }),

            clinicDog: new L.Icon({ iconUrl:"https://maps.google.com/mapfiles/ms/icons/blue-dot.png", iconSize:[32,32] }),
            clinicCat: new L.Icon({ iconUrl:"https://maps.google.com/mapfiles/ms/icons/blue-dot.png", iconSize:[32,32] })
        };

        // ==== TU CLÍNICA ====
        if(data.reporte_actual){

            const especieClinica = razas.Perro.includes(data.reporte_actual.raza) ? "Dog" : "Cat";

            L.marker(
                [data.reporte_actual.latitud, data.reporte_actual.longitud],
                {icon: icons["clinic" + especieClinica]}
            ).addTo(currentMap)
            .bindPopup(`<b>🏥 Tu clínica</b><br>Raza: ${data.reporte_actual.raza}<br><img src="/${data.reporte_actual.path_imagen}" width="180">`);

        }

        // ==== MASCOTAS PERDIDAS ====
        data.perdidos
            .filter(p => !maxDistance || !p.distancia_km || p.distancia_km <= maxDistance)
            .filter(p => {
                if(currentSpecies === "all") return true;
                if(currentSpecies === "Perro") return razas.Perro.includes(p.raza);
                if(currentSpecies === "Gato") return razas.Gato.includes(p.raza);
            })
            .forEach(p => {
                const especie = razas.Perro.includes(p.raza) ? "Dog" : "Cat";
                L.marker([p.latitud, p.longitud], {icon: icons["lost" + especie]})
                .addTo(currentMap)
                .bindPopup(`<b>🐾 Mascota perdida</b><br>Raza: ${p.raza}<br>Usuario: ${p.usuario}<br>${p.distancia_km ? "Distancia: " + p.distancia_km.toFixed(2) + " km<br>" : ""}<br><img src="/${p.path_imagen}" width="150">`);
            });

        // ==== MASCOTAS PROTEGIDAS / CLÍNICAS ASOCIADAS ====
        data.protegidos
            .filter(p => !maxDistance || !p.distancia_km || p.distancia_km <= maxDistance)
            .filter(p => {
                if(currentSpecies === "all") return true;
                if(currentSpecies === "Perro") return razas.Perro.includes(p.raza);
                if(currentSpecies === "Gato") return razas.Gato.includes(p.raza);
            })
            .forEach(p => {
                const especie = razas.Perro.includes(p.raza) ? "Dog" : "Cat";
                L.marker([p.latitud, p.longitud], {icon: icons["shelter" + especie]})
                .addTo(currentMap)
                .bindPopup(`<b>🏥 Clínica asociada</b><br>Raza: ${p.raza}<br>Protectora: ${p.protectora}<br>${p.distancia_km ? "Distancia: " + p.distancia_km.toFixed(2) + " km<br>" : ""}<br><img src="/${p.path_imagen}" width="150">`);
            });
    }

    // Botón Analizar
    analyzeBtn.addEventListener("click", function(){
        const file = fileInput.files[0];
        if(!file){ message.textContent="Selecciona una imagen"; message.style.color="red"; return; }

        message.textContent="Solicitando ubicación...";
        if(!navigator.geolocation){ message.textContent="Geolocalización no soportada"; return; }

        navigator.geolocation.getCurrentPosition(async function(position){
            const formData = new FormData();
            formData.append("imagen", file);
            formData.append("latitud", position.coords.latitude);
            formData.append("longitud", position.coords.longitude);

            try{
                const response = await fetch("/report",{method:"POST",body:formData});
                if(!response.ok) throw new Error("Error servidor");
                const data = await response.json();
                backendData = data;
                drawMap(data);
                // Activar filtros de distancia
                distanceButtons.forEach(btn => {
                    btn.disabled = false;
                    btn.style.opacity = 1;
                    btn.style.cursor = "pointer";
                });
                message.textContent="Reporte registrado ✅";
                message.style.color="green";
            }catch(err){ message.textContent="Error al procesar " + err.message; message.style.color="red"; }
        }, function(){ message.textContent="No se pudo obtener ubicación"; message.style.color="red"; });
    });

    // ===== FILTRO DE DISTANCIA =====
    document.querySelectorAll(".distance-filter button").forEach(btn => {
        btn.addEventListener("click", function() {
            // Quitar clase active de todos los botones
            document.querySelectorAll(".distance-filter button").forEach(b => b.classList.remove("active"));

            // Activar este botón
            this.classList.add("active");

            // Redibujar mapa solo si hay datos cargados
            if (!backendData) return;

            const km = this.dataset.km;
        if(km === "all") {
            drawMap(backendData); // Sin filtrar
        } else {
            drawMap(backendData, parseInt(km)); // Filtrar por distancia
        }
        });
    });

    document.querySelectorAll(".species-filter button").forEach(btn => {

        btn.addEventListener("click", function(){

            document.querySelectorAll(".species-filter button")
            .forEach(b => b.classList.remove("active"));

            this.classList.add("active");

            currentSpecies = this.dataset.species;

            if(!backendData) return;

            const activeDistance = document.querySelector(".distance-filter button.active").dataset.km;

            drawMap(
                backendData,
                activeDistance === "all" ? Infinity : parseInt(activeDistance)
            );

        });

    });

    fetch("/shelter/maps")
.then(res => res.json())
.then(data => {

    backendData = {
        reporte_actual: null,
        perdidos: data.perdidos,
        protegidos: data.protegidos
    };

    // usar primer punto para centrar mapa
        if(data.protegidos.length > 0){
            backendData.reporte_actual = data.protegidos[0];
        } else if(data.perdidos.length > 0){
            backendData.reporte_actual = data.perdidos[0];
        }

        drawMap(backendData);

    });

});