import os
import sys
# DON'T CHANGE THIS !!!
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from flask import Flask, send_from_directory
from flask_cors import CORS
from src.models.models import db
from src.routes.dogs import dogs_bp
from src.routes.owners import owners_bp

app = Flask(__name__, static_folder=os.path.join(os.path.dirname(__file__), 'static'))
app.config['SECRET_KEY'] = 'asdf#FGSgvasgf$5$WGT'

# Configurar CORS para permitir acceso desde cualquier origen
CORS(app)

# Registrar blueprints
app.register_blueprint(dogs_bp, url_prefix='/api')
app.register_blueprint(owners_bp, url_prefix='/api')

# Configuración de base de datos
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:123456789@localhost/new_schema' 
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)
with app.app_context():
    db.create_all()
    
    # Agregar datos de ejemplo si no existen
    from src.models.models import Dueno, Perro
    if Dueno.query.count() == 0:
        # Crear dueños de ejemplo
        duenos_ejemplo = [
            Dueno(nombre='Juan Pérez'),
            Dueno(nombre='María García'),
            Dueno(nombre='Carlos López'),
            Dueno(nombre='Ana Martínez'),
            Dueno(nombre='Luis Rodríguez')
        ]
        
        for dueno in duenos_ejemplo:
            db.session.add(dueno)
        
        db.session.commit()
        
        # Crear perros de ejemplo
        perros_ejemplo = [
            Perro(nombre='Max', raza='Labrador', tamano='Grande', comportamiento='Amigable y juguetón', calle='Calle 123', edad=3, dueno_id=1),
            Perro(nombre='Bella', raza='Chihuahua', tamano='Pequeño', comportamiento='Protectora y leal', calle='Avenida Central', edad=2, dueno_id=2),
            Perro(nombre='Rocky', raza='Pastor Alemán', tamano='Grande', comportamiento='Obediente y guardián', calle='Calle Principal', edad=5, dueno_id=3),
            Perro(nombre='Luna', raza='Golden Retriever', tamano='Grande', comportamiento='Cariñosa y energética', calle='Calle 456', edad=4, dueno_id=1),
            Perro(nombre='Toby', raza='Beagle', tamano='Mediano', comportamiento='Curioso y activo', calle='Calle Secundaria', edad=1, dueno_id=4),
            Perro(nombre='Coco', raza='Poodle', tamano='Mediano', comportamiento='Inteligente y elegante', calle='Avenida Norte', edad=6, dueno_id=5),
            Perro(nombre='Rex', raza='Bulldog', tamano='Mediano', comportamiento='Tranquilo y amigable', calle='Calle Sur', edad=3, dueno_id=2),
            Perro(nombre='Mila', raza='Husky', tamano='Grande', comportamiento='Independiente y activa', calle='Calle Este', edad=2, dueno_id=3)
        ]
        
        for perro in perros_ejemplo:
            db.session.add(perro)
        
        db.session.commit()

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def serve(path):
    static_folder_path = app.static_folder
    if static_folder_path is None:
            return "Static folder not configured", 404

    if path != "" and os.path.exists(os.path.join(static_folder_path, path)):
        return send_from_directory(static_folder_path, path)
    else:
        index_path = os.path.join(static_folder_path, 'index.html')
        if os.path.exists(index_path):
            return send_from_directory(static_folder_path, 'index.html')
        else:
            return "index.html not found", 404


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
