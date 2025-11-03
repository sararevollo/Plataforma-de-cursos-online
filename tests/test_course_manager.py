import sys
sys.path.insert(0, '../src')

from models.course_manager import CourseManager, CourseValidationError


def test_create_course():
    """Test creación de curso"""
    manager = CourseManager()
    
    course = manager.create_course(
        course_id="test_001",
        title="Curso de Prueba Completo",
        description="Esta es una descripción de prueba con más de 50 caracteres para cumplir validación.",
        instructor_id="inst_001",
        price=99.99
    )
    
    assert course.course_id == "test_001"
    assert course.price == 99.99
    print("✓ Test create_course pasado")


def test_search_courses():
    """Test búsqueda de cursos"""
    manager = CourseManager()
    
    manager.create_course(
        "curso1",
        "Python Avanzado Para Todos",
        "Descripción del curso de Python con contenido avanzado y completo.",
        "inst1",
        49.99
    )
    
    results = manager.search_courses(keyword="Python")
    assert len(results) == 1
    print("✓ Test search_courses pasado")


if __name__ == "__main__":
    test_create_course()
    test_search_courses()
    print("\n✅ Todos los tests pasaron correctamente")
