from datetime import datetime
from typing import List, Dict, Optional
import logging

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class CourseValidationError(Exception):
    """Excepción personalizada para errores de validación de cursos"""
    pass


class Course:
    """
    Representa un curso en la plataforma educativa.
    
    Attributes:
        course_id (str): Identificador único del curso
        title (str): Título del curso
        description (str): Descripción detallada
        instructor_id (str): ID del instructor propietario
        price (float): Precio del curso
        level (str): Nivel de dificultad
        category (str): Categoría del curso
    """
    
    VALID_LEVELS = ['principiante', 'intermedio', 'avanzado']
    VALID_CATEGORIES = [
        'programacion', 'diseno', 'negocios', 'marketing', 
        'desarrollo-personal', 'idiomas', 'ciencias'
    ]
    
    def __init__(
        self, 
        course_id: str,
        title: str,
        description: str,
        instructor_id: str,
        price: float = 0.0,
        level: str = 'principiante',
        category: str = 'programacion'
    ):
        """Inicializa un nuevo curso con sus atributos básicos"""
        self.course_id = course_id
        self.title = title
        self.description = description
        self.instructor_id = instructor_id
        self.price = price
        self.level = level
        self.category = category
        self.created_at = datetime.now()
        self.updated_at = datetime.now()
        self.modules: List[Dict] = []
        self.students_enrolled: List[str] = []
        self.rating: float = 0.0
        self.total_reviews: int = 0
        
    def to_dict(self) -> Dict:
        """Convierte el curso a un diccionario para serialización"""
        return {
            'course_id': self.course_id,
            'title': self.title,
            'description': self.description,
            'instructor_id': self.instructor_id,
            'price': self.price,
            'level': self.level,
            'category': self.category,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat(),
            'modules': self.modules,
            'students_count': len(self.students_enrolled),
            'rating': self.rating,
            'total_reviews': self.total_reviews
        }

class CourseManager:
    """
    Gestiona operaciones CRUD y lógica de negocio para cursos.
    Implementa principios de código limpio y responsabilidad única.
    """
    
    def __init__(self):
        """Inicializa el gestor con almacenamiento en memoria"""
        self.courses: Dict[str, Course] = {}
        logger.info("CourseManager inicializado correctamente")
    
    def _validate_course_data(
        self,
        title: str,
        description: str,
        price: float,
        level: str,
        category: str
    ) -> None:
        """
        Valida los datos del curso según reglas de negocio.
        Función privada para mantener código limpio.
        """
        # Validar título
        if not title or len(title.strip()) < 10:
            raise CourseValidationError(
                "El título debe tener al menos 10 caracteres"
            )
        
        # Validar descripción
        if not description or len(description.strip()) < 50:
            raise CourseValidationError(
                "La descripción debe tener al menos 50 caracteres"
            )
        
        # Validar precio
        if price < 0:
            raise CourseValidationError(
                "El precio no puede ser negativo"
            )
        
        # Validar nivel
        if level.lower() not in Course.VALID_LEVELS:
            raise CourseValidationError(
                f"Nivel inválido. Debe ser uno de: {Course.VALID_LEVELS}"
            )
        
        # Validar categoría
        if category.lower() not in Course.VALID_CATEGORIES:
            raise CourseValidationError(
                f"Categoría inválida. Debe ser una de: {Course.VALID_CATEGORIES}"
            )

	def create_course(
        self,
        course_id: str,
        title: str,
        description: str,
        instructor_id: str,
        price: float = 0.0,
        level: str = 'principiante',
        category: str = 'programacion'
    ) -> Course:
        """
        Crea un nuevo curso con validación completa.
        
        Args:
            course_id: ID único del curso
            title: Título del curso (mínimo 10 caracteres)
            description: Descripción (mínimo 50 caracteres)
            instructor_id: ID del instructor
            price: Precio del curso (debe ser >= 0)
            level: Nivel de dificultad
            category: Categoría del curso
            
        Returns:
            Course: Objeto curso creado
            
        Raises:
            CourseValidationError: Si los datos no son válidos
        """
        try:
            # Validar que el curso no exista
            if course_id in self.courses:
                raise CourseValidationError(
                    f"El curso con ID {course_id} ya existe"
                )
            
            # Validar datos de entrada
            self._validate_course_data(
                title, description, price, level, category
            )
            
            # Crear el curso
            new_course = Course(
                course_id=course_id,
                title=title,
                description=description,
                instructor_id=instructor_id,
                price=price,
                level=level.lower(),
                category=category.lower()
            )
            
            # Almacenar el curso
            self.courses[course_id] = new_course
            
            logger.info(f"Curso creado exitosamente: {course_id}")
            return new_course
            
        except Exception as e:
            logger.error(f"Error al crear curso: {str(e)}")
            raise