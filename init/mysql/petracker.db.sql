CREATE DATABASE IF NOT EXISTS perros_app CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
CREATE DATABASE IF NOT EXISTS perros_test CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

USE perros_app;

CREATE TABLE IF NOT EXISTS usuarios (
  nombre VARCHAR(50) PRIMARY KEY,
  contrasena_hash VARCHAR(255) NOT NULL
);

CREATE TABLE IF NOT EXISTS protectoras (
  nombre VARCHAR(50) PRIMARY KEY,
  contrasena_hash VARCHAR(255) NOT NULL
);

CREATE TABLE IF NOT EXISTS mascotas_perdidas (
  id INT NOT NULL AUTO_INCREMENT,
  username VARCHAR(50) NOT NULL,
  raza VARCHAR(50),
  latitud DECIMAL(9,6),
  longitud DECIMAL(9,6),
  path_imagen VARCHAR(255) NOT NULL,
  fecha TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (id),
  FOREIGN KEY (username) REFERENCES usuarios(nombre) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS mascotas_acogidas (
  id INT NOT NULL AUTO_INCREMENT,
  protectora VARCHAR(50) NOT NULL,
  raza VARCHAR(50),
  latitud DECIMAL(9,6),
  longitud DECIMAL(9,6),
  path_imagen VARCHAR(255) NOT NULL,
  fecha TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (id),
  FOREIGN KEY (protectora) REFERENCES protectoras(nombre) ON DELETE CASCADE
);

INSERT INTO usuarios (nombre, contrasena_hash) VALUES
('carlos','1234'),('juan','abcd'),('maria','5678');

INSERT INTO protectoras (nombre, contrasena_hash) VALUES
('huellas','4321'),('patas_felices','9876');

INSERT INTO mascotas_perdidas VALUES
(1,'juan','labrador',40.416775,-3.703790,'static/uploads/juan/labrador1.png','2026-02-04 08:32:36'),
(2,'juan','siamese',40.418000,-3.700000,'static/uploads/juan/siamese1.png','2026-02-04 08:32:36'),
(3,'maria','beagle',41.387397,2.168568,'static/uploads/maria/beagle1.png','2026-02-04 08:32:36'),
(4,'carlos','poodle',37.389092,-5.984459,'static/uploads/carlos/poodle1.png','2026-02-04 08:32:36');

INSERT INTO mascotas_acogidas VALUES
(1,'patas_felices','siamese',40.400000,-3.700000,'static/shelters_uploads/patas_felices/mascota1.png','2026-02-04 08:32:36'),
(2,'patas_felices','beagle',40.401000,-3.702000,'static/shelters_uploads/patas_felices/mascota2.png','2026-02-04 08:32:36'),
(3,'huellas','beagle',41.380000,2.170000,'static/shelters_uploads/huellas/mascota1.png','2026-02-04 08:32:36'),
(4,'huellas','bengal',41.382000,2.175000,'static/shelters_uploads/huellas/mascota2.png','2026-02-04 08:32:36'),
(5,'patas_felices','retriever',38.000000,-4.000000,'static/shelters_uploads/patas_felices/mascota3.png','2026-02-04 08:32:36');

USE perros_test;

CREATE TABLE IF NOT EXISTS usuarios (
  nombre VARCHAR(50) PRIMARY KEY,
  contrasena_hash VARCHAR(255) NOT NULL
);

CREATE TABLE IF NOT EXISTS protectoras (
  nombre VARCHAR(50) PRIMARY KEY,
  contrasena_hash VARCHAR(255) NOT NULL
);

CREATE TABLE IF NOT EXISTS mascotas_perdidas (
  id INT NOT NULL AUTO_INCREMENT,
  username VARCHAR(50) NOT NULL,
  raza VARCHAR(50),
  latitud DECIMAL(9,6),
  longitud DECIMAL(9,6),
  path_imagen VARCHAR(255) NOT NULL,
  fecha TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (id),
  FOREIGN KEY (username) REFERENCES usuarios(nombre) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS mascotas_acogidas (
  id INT NOT NULL AUTO_INCREMENT,
  protectora VARCHAR(50) NOT NULL,
  raza VARCHAR(50),
  latitud DECIMAL(9,6),
  longitud DECIMAL(9,6),
  path_imagen VARCHAR(255) NOT NULL,
  fecha TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (id),
  FOREIGN KEY (protectora) REFERENCES protectoras(nombre) ON DELETE CASCADE
);