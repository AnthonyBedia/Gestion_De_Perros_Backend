from flask import Blueprint, request, jsonify
from src.models.models import db, Perro, Dueno
from sqlalchemy import func

dogs_bp = Blueprint('dogs', __name__)

@dogs_bp.route('/perros', methods=['GET'])
def get_perros():
    """Obtener todos los perros con filtros opcionales"""
    try:
        # Parámetros de filtro
        nombre = request.args.get('nombre')
        raza = request.args.get('raza')
        tamano = request.args.get('tamano')
        comportamiento = request.args.get('comportamiento')
        calle = request.args.get('calle')
        dueno_nombre = request.args.get('dueno')
        
        # Construir query base
        query = Perro.query.join(Dueno)
        
        # Aplicar filtros
        if nombre:
            query = query.filter(Perro.nombre.ilike(f'%{nombre}%'))
        if raza:
            query = query.filter(Perro.raza.ilike(f'%{raza}%'))
        if tamano:
            query = query.filter(Perro.tamano == tamano)
        if comportamiento:
            query = query.filter(Perro.comportamiento.ilike(f'%{comportamiento}%'))
        if calle:
            query = query.filter(Perro.calle.ilike(f'%{calle}%'))
        if dueno_nombre:
            query = query.filter(Dueno.nombre.ilike(f'%{dueno_nombre}%'))
        
        perros = query.all()
        return jsonify([perro.to_dict() for perro in perros])
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@dogs_bp.route('/perros', methods=['POST'])
def create_perro():
    """Crear un nuevo perro y su dueño si no existe"""
    try:
        data = request.get_json()
        
        # Validar datos requeridos
        required_fields = ['nombre', 'raza', 'tamano', 'dueno_nombre']
        for field in required_fields:
            if field not in data or not data[field]:
                return jsonify({'error': f'Campo requerido: {field}'}), 400
        
        # Buscar o crear dueño
        dueno = Dueno.query.filter_by(nombre=data['dueno_nombre']).first()
        if not dueno:
            dueno = Dueno(nombre=data['dueno_nombre'])
            db.session.add(dueno)
            db.session.flush()  # Para obtener el ID
        
        # Crear perro
        perro = Perro(
            nombre=data['nombre'],
            raza=data['raza'],
            tamano=data['tamano'],
            comportamiento=data.get('comportamiento', ''),
            calle=data.get('calle', ''),
            edad=data.get('edad'),
            dueno_id=dueno.id
        )
        
        db.session.add(perro)
        db.session.commit()
        
        return jsonify(perro.to_dict()), 201
    
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@dogs_bp.route('/perros/<int:perro_id>', methods=['PUT'])
def update_perro(perro_id):
    """Actualizar un perro existente"""
    try:
        perro = Perro.query.get_or_404(perro_id)
        data = request.get_json()
        
        # Actualizar campos
        if 'nombre' in data:
            perro.nombre = data['nombre']
        if 'raza' in data:
            perro.raza = data['raza']
        if 'tamano' in data:
            perro.tamano = data['tamano']
        if 'comportamiento' in data:
            perro.comportamiento = data['comportamiento']
        if 'calle' in data:
            perro.calle = data['calle']
        if 'edad' in data:
            perro.edad = data['edad']
        
        db.session.commit()
        return jsonify(perro.to_dict())
    
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@dogs_bp.route('/perros/<int:perro_id>', methods=['DELETE'])
def delete_perro(perro_id):
    """Eliminar un perro"""
    try:
        perro = Perro.query.get_or_404(perro_id)
        db.session.delete(perro)
        db.session.commit()
        return jsonify({'message': 'Perro eliminado exitosamente'})
    
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@dogs_bp.route('/dashboard/stats', methods=['GET'])
def get_dashboard_stats():
    """Obtener estadísticas para el dashboard"""
    try:
        # Total de perros registrados
        total_perros = Perro.query.count()
        
        # Perros por raza
        perros_por_raza = db.session.query(
            Perro.raza,
            func.count(Perro.id).label('count')
        ).group_by(Perro.raza).all()
        
        # Categorías de edad
        categorias_edad = []
        cachorros = Perro.query.filter(Perro.edad <= 1).count()  # 0-1 años
        jovenes = Perro.query.filter(Perro.edad.between(2, 3)).count()  # 2-3 años
        adultos = Perro.query.filter(Perro.edad.between(4, 7)).count()  # 4-7 años
        seniors = Perro.query.filter(Perro.edad >= 8).count()  # 8+ años
        sin_edad = Perro.query.filter(Perro.edad.is_(None)).count()  # Sin edad especificada
        
        categorias_edad = [
            {'categoria': 'Cachorros (0-1 años)', 'count': cachorros},
            {'categoria': 'Jóvenes (2-3 años)', 'count': jovenes},
            {'categoria': 'Adultos (4-7 años)', 'count': adultos},
            {'categoria': 'Seniors (8+ años)', 'count': seniors},
            {'categoria': 'Sin edad especificada', 'count': sin_edad}
        ]
        
        return jsonify({
            'total_perros': total_perros,
            'perros_por_raza': [{'raza': raza, 'count': count} for raza, count in perros_por_raza],
            'categorias_edad': categorias_edad
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

