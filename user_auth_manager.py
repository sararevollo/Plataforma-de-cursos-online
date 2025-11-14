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

class SessionManager:
    """Gestiona sesiones y tokens de autenticación."""
    
    def __init__(self, session_duration_hours: int = 24):
        self.sessions: Dict[str, Dict] = {}
        self.session_duration = timedelta(hours=session_duration_hours)
    
    def create_session(self, user_id: str) -> str:
        """Crea nueva sesión para usuario."""
        token = secrets.token_urlsafe(32)
        expiry = datetime.now() + self.session_duration
        
        self.sessions[token] = {
            'user_id': user_id,
            'created_at': datetime.now(),
            'expires_at': expiry
        }
        
        logger.info(f"Sesión creada para {user_id}")
        return token
    
    def validate_session(self, token: str) -> Optional[str]:
        """Valida token de sesión."""
        session = self.sessions.get(token)
        
        if not session:
            return None
        
        if datetime.now() > session['expires_at']:
            self.revoke_session(token)
            return None
        
        return session['user_id']
    
    def revoke_session(self, token: str) -> bool:
        """Revoca sesión (logout)."""
        if token in self.sessions:
            del self.sessions[token]
            return True
        return False

class UserManager:
    """Gestiona operaciones CRUD de usuarios."""
    
    def __init__(self):
        self.users: Dict[str, User] = {}
        self.email_index: Dict[str, str] = {}
        self.session_manager = SessionManager()
        logger.info("UserManager inicializado")
    
    def register_user(
        self, email: str, password: str, name: str, user_type: str = 'student'
    ) -> User:
        """Registra nuevo usuario."""
        self._validate_email(email)
        
        if email in self.email_index:
            raise ValidationError(f"Email {email} ya registrado")
        
        PasswordManager.validate_password_strength(password)
        
        user_id = f"user_{secrets.token_hex(8)}"
        password_hash = PasswordManager.hash_password(password)
        
        new_user = User(user_id, email, password_hash, name, user_type)
        
        self.users[user_id] = new_user
        self.email_index[email] = user_id
        
        logger.info(f"Usuario registrado: {email}")
        return new_user
    
    def _validate_email(self, email: str) -> bool:
        """Valida formato de email."""
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not re.match(pattern, email):
            raise ValidationError("Email inválido")
        return True
    
    def login(self, email: str, password: str) -> Dict:
        """Autentica usuario."""
        user_id = self.email_index.get(email)
        
        if not user_id:
            raise AuthenticationError("Credenciales incorrectas")
        
        user = self.users[user_id]
        
        if not PasswordManager.verify_password(password, user.password_hash):
            raise AuthenticationError("Credenciales incorrectas")
        
        user.last_login = datetime.now()
        token = self.session_manager.create_session(user_id)
        
        return {'token': token, 'user': user.to_dict()}