from djangosaml2.backends import Saml2Backend
from django.contrib.auth import get_user_model
from django.db import transaction
from .models import UserProfile, University, StudyField

User = get_user_model()

class SurfConextSaml2Backend(Saml2Backend):
    """
    Custom SAML backend for SurfConext integration.
    Handles user creation and attribute mapping from Dutch universities.
    """
    
    def configure_user(self, user, attributes, attribute_mapping):
        """
        Configure user with attributes from SAML response.
        """
        # Map basic user attributes
        if 'first_name' in attributes:
            user.first_name = attributes['first_name'][0]
        if 'last_name' in attributes:
            user.last_name = attributes['last_name'][0]
        if 'email' in attributes:
            user.email = attributes['email'][0]
        
        # Generate username from email if not provided
        if not user.username and 'email' in attributes:
            email = attributes['email'][0]
            user.username = email.split('@')[0]
        
        # Ensure username is unique
        if user.username:
            original_username = user.username
            counter = 1
            while User.objects.filter(username=user.username).exists():
                user.username = f"{original_username}{counter}"
                counter += 1
        
        user.save()
        
        # Create or update user profile
        self._update_user_profile(user, attributes)
        
        return user
    
    def _update_user_profile(self, user, attributes):
        """
        Update user profile with university and study information.
        """
        try:
            profile = user.profile
        except UserProfile.DoesNotExist:
            profile = UserProfile.objects.create(user=user)
        
        # Map university from schacHomeOrganization
        if 'university' in attributes:
            university_code = attributes['university'][0]
            university, created = University.objects.get_or_create(
                code=university_code,
                defaults={
                    'name': self._get_university_name(university_code),
                    'is_active': True
                }
            )
            profile.university = university
        
        # Map student ID from schacPersonalUniqueCode
        if 'student_id' in attributes:
            student_id = attributes['student_id'][0]
            # Extract student number from schacPersonalUniqueCode
            # Format: urn:schac:personalUniqueCode:nl:institution:student_number
            if ':' in student_id:
                parts = student_id.split(':')
                if len(parts) >= 6:
                    profile.student_id = parts[-1]
        
        # Set study level based on email domain or other attributes
        if 'email' in attributes:
            email = attributes['email'][0]
            if '@student.' in email or '@students.' in email:
                profile.study_level = 'bachelor'
            elif '@alumni.' in email:
                profile.study_level = 'alumni'
            else:
                profile.study_level = 'other'
        
        profile.save()
    
    def _get_university_name(self, code):
        """
        Map university codes to names.
        """
        university_names = {
            'tudelft.nl': 'TU Delft',
            'uva.nl': 'University of Amsterdam',
            'uu.nl': 'Utrecht University',
            'tue.nl': 'Eindhoven University of Technology',
            'tudelft.nl': 'TU Delft',
            'wur.nl': 'Wageningen University & Research',
            'ru.nl': 'Radboud University',
            'vu.nl': 'Vrije Universiteit Amsterdam',
            'leidenuniv.nl': 'Leiden University',
            'rug.nl': 'University of Groningen',
            'maastrichtuniversity.nl': 'Maastricht University',
            'tilburguniversity.edu': 'Tilburg University',
            'ou.nl': 'Open University',
            'fontys.nl': 'Fontys University of Applied Sciences',
            'han.nl': 'HAN University of Applied Sciences',
            'hva.nl': 'Amsterdam University of Applied Sciences',
            'hr.nl': 'Rotterdam University of Applied Sciences',
            'hu.nl': 'Utrecht University of Applied Sciences',
            'windesheim.nl': 'Windesheim University of Applied Sciences',
        }
        return university_names.get(code, code)
    
    def update_user(self, user, created, attributes, attribute_mapping, force_save=False):
        """
        Update existing user with new attributes.
        """
        if not created:
            self._update_user_profile(user, attributes)
        
        return super().update_user(user, created, attributes, attribute_mapping, force_save) 