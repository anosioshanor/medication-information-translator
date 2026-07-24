class Medication:
    """
    Medication class representing a medication with its properties
    """
    
    def __init__(self, name, uses=None, warnings=None, side_effects=None):
        """
        Initialize a Medication object
        
        Args:
            name (str): Medication name
            uses (list): List of uses
            warnings (list): List of warnings
            side_effects (list): List of side effects
        """
        self._name = name
        self._uses = uses or []
        self._warnings = warnings or []
        self._side_effects = side_effects or []
        self._is_generic = False
    
    @property
    def name(self):
        """Get medication name"""
        return self._name
    
    @name.setter
    def name(self, value):
        """Set medication name with validation"""
        if not value or len(value.strip()) < 2:
            raise ValueError("Medication name must be at least 2 characters")
        self._name = value.strip()
    
    def display_name(self):
        """Return formatted display name"""
        return self._name.title()
    
    def add_use(self, use):
        """Add a use to the medication"""
        if use and use not in self._uses:
            self._uses.append(use)
    
    def add_warning(self, warning):
        """Add a warning to the medication"""
        if warning and warning not in self._warnings:
            self._warnings.append(warning)
    
    def add_side_effect(self, side_effect):
        """Add a side effect to the medication"""
        if side_effect and side_effect not in self._side_effects:
            self._side_effects.append(side_effect)
    
    def get_uses(self):
        """Get all uses"""
        return self._uses.copy()
    
    def get_warnings(self):
        """Get all warnings"""
        return self._warnings.copy()
    
    def get_side_effects(self):
        """Get all side effects"""
        return self._side_effects.copy()
    
    def to_dict(self):
        """Convert medication to dictionary"""
        return {
            "name": self._name,
            "uses": self._uses,
            "warnings": self._warnings,
            "side_effects": self._side_effects
        }
    
    def __str__(self):
        """String representation of the medication"""
        return f"Medication: {self.display_name()}"
    
    def __repr__(self):
        """Detailed representation of the medication"""
        return f"Medication(name='{self._name}', uses={len(self._uses)}, warnings={len(self._warnings)})"
