from flask import Blueprint, request, jsonify
from src.models.models import db, Dueno, Perro

owners_bp = Blueprint('owners', __name__)

@owners_bp.route('/duenos', methods=['GET'])
def get_duenos():
    """Obtener todos los dueños"""
    try:
        duenos = Dueno.query.all()
        return jsonify([dueno.to_dict() for dueno in duenos])
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@owners_bp.route('/duenos', methods=['POST'])
def create_dueno():
    """Crear un nuevo dueño"""
    try:
        data = request.get_json()
        
        # Validar datos requeridos
        if 'nombre' not in data or not data['nombre']:
            return jsonify({'error': 'Campo requerido: nombre'}), 400
        
        # Verificar si ya existe
        existing_dueno = Dueno.query.filter_by(nombre=data['nombre']).first()
        if existing_dueno:
            return jsonify({'error': 'Ya existe un dueño con ese nombre'}), 400
        
        # Crear dueño
        dueno = Dueno(nombre=data['nombre'])
        db.session.add(dueno)
        db.session.commit()
        
        return jsonify(dueno.to_dict()), 201
    
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@owners_bp.route('/duenos/<int:dueno_id>', methods=['GET'])
def get_dueno(dueno_id):
    """Obtener un dueño específico con sus perros"""
    try:
        dueno = Dueno.query.get_or_404(dueno_id)
        return jsonify(dueno.to_dict())
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@owners_bp.route('/duenos/<int:dueno_id>', methods=['PUT'])
def update_dueno(dueno_id):
    """Actualizar un dueño existente"""
    try:
        dueno = Dueno.query.get_or_404(dueno_id)
        data = request.get_json()
        
        if 'nombre' in data:
            dueno.nombre = data['nombre']
        
        db.session.commit()
        return jsonify(dueno.to_dict())
    
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@owners_bp.route('/duenos/<int:dueno_id>', methods=['DELETE'])
def delete_dueno(dueno_id):
    """Eliminar un dueño y todos sus perros"""
    try:
        dueno = Dueno.query.get_or_404(dueno_id)
        db.session.delete(dueno)
        db.session.commit()
        return jsonify({'message': 'Dueño eliminado exitosamente'})
    
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

