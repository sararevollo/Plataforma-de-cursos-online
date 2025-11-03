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