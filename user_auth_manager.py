import hashlib
import secrets
import re
from datetime import datetime, timedelta
from typing import Dict, Optional, List
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class AuthenticationError(Exception):
    """Excepción para errores de autenticación"""
    pass


class ValidationError(Exception):
    """Excepción para errores de validación"""
    pass


class User:
    """Representa un usuario en el sistema."""
    
    VALID_USER_TYPES = ['student', 'instructor', 'admin']
    
    def __init__(
        self,
        user_id: str,
        email: str,
        password_hash: str,
        name: str,
        user_type: str = 'student'
    ):
        self.user_id = user_id
        self.email = email
        self.password_hash = password_hash
        self.name = name
        self.user_type = user_type
        self.created_at = datetime.now()
        self.last_login: Optional[datetime] = None
        self.is_active = True
        self.enrolled_courses: List[str] = []
        
    def to_dict(self) -> Dict:
        """Convierte usuario a diccionario"""
        return {
            'user_id': self.user_id,
            'email': self.email,
            'name': self.name,
            'user_type': self.user_type,
            'created_at': self.created_at.isoformat(),
            'is_active': self.is_active
        }

class PasswordManager:
    """Gestiona operaciones de contraseñas de forma segura."""
    
    MIN_PASSWORD_LENGTH = 8
    
    @staticmethod
    def hash_password(password: str) -> str:
        """
        Genera hash seguro usando SHA-256 con salt.
        
        Args:
            password: Contraseña en texto plano
            
        Returns:
            Hash con salt incluido
        """
        salt = secrets.token_hex(16)
        pwd_hash = hashlib.sha256((password + salt).encode()).hexdigest()
        return f"{salt}${pwd_hash}"
    
    @staticmethod
    def verify_password(password: str, stored_hash: str) -> bool:
        """
        Verifica si contraseña coincide con hash.
        
        Args:
            password: Contraseña a verificar
            stored_hash: Hash almacenado
            
        Returns:
            True si la contraseña es correcta
        """
        try:
            salt, pwd_hash = stored_hash.split('$')
            computed_hash = hashlib.sha256(
                (password + salt).encode()
            ).hexdigest()
            return computed_hash == pwd_hash
        except ValueError:
            logger.error("Formato de hash inválido")
            return False
    
    @classmethod
    def validate_password_strength(cls, password: str) -> bool:
        """Valida fortaleza de contraseña."""
        if len(password) < cls.MIN_PASSWORD_LENGTH:
            raise ValidationError(
                f"Contraseña debe tener {cls.MIN_PASSWORD_LENGTH}+ caracteres"
            )
        
        if not re.search(r'[A-Z]', password):
            raise ValidationError("Debe contener una mayúscula")
        
        if not re.search(r'[a-z]', password):
            raise ValidationError("Debe contener una minúscula")
        
        if not re.search(r'\d', password):
            raise ValidationError("Debe contener un número")
        
        return True