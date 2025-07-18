"""
SAML Configuration for SurfConext Integration
This file contains the SAML settings for StudentZone
"""

import os
from django.conf import settings

# Base directory for certificates
CERTS_DIR = os.path.join(settings.BASE_DIR, 'certs')
PRIVATE_KEY_PATH = os.path.join(CERTS_DIR, 'private.key')
CERT_PATH = os.path.join(CERTS_DIR, 'certificate.crt')

# SAML Configuration
SAML_CONFIG = {
    'debug': settings.DEBUG,
    'xmlsec_binary': None,  # Will be auto-detected
    'entityid': 'https://studentzone.local/saml2/metadata/',
    'description': 'StudentZone - Nationwide Student Network for Dutch Higher Education',
    'service': {
        'sp': {
            'name': 'StudentZone',
            'endpoints': {
                'assertion_consumer_service': [
                    ('https://studentzone.local/saml2/acs/', 'urn:oasis:names:tc:SAML:2.0:bindings:HTTP-POST'),
                ],
                'single_logout_service': [
                    ('https://studentzone.local/saml2/ls/', 'urn:oasis:names:tc:SAML:2.0:bindings:HTTP-Redirect'),
                    ('https://studentzone.local/saml2/ls/post/', 'urn:oasis:names:tc:SAML:2.0:bindings:HTTP-POST'),
                ],
            },
            'name_id_format': 'urn:oasis:names:tc:SAML:2.0:nameid-format:transient',
            'name_id_format_allow_create': False,
            'authn_requests_signed': False,
            'want_assertions_signed': False,  # Disabled for development
            'want_response_signed': False,
            'want_assertions_or_response_signed': False,  # Disabled for development
            'want_name_id': True,
            'want_name_id_format': None,
            'want_attribute_statement': True,
            'want_subject_confirmation': True,
            'want_subject_confirmation_in_response': True,
            'want_subject_confirmation_in_assertions': True,
            'want_encrypted_assertion': False,
            'want_encrypted_name_id': False,
            'want_encrypted_attributes': False,
            'want_digest': False,  # Disabled for development
            'want_signature_validation': False,  # Disabled for development
            'metadata_local': None,
            'metadata': {
                'remote': [
                    {
                        'url': 'https://metadata.surfconext.nl/entities',
                        'cert': None,
                    },
                ],
            },
            'attribute_map_dir': None,
            'attribute_map': {
                'uid': 'username',
                'mail': 'email',
                'cn': 'first_name',
                'sn': 'last_name',
                'schacHomeOrganization': 'university',
                'schacPersonalUniqueCode': 'student_id',
                'displayName': 'display_name',
                'givenName': 'first_name',
                'surname': 'last_name',
            },
        },
    },
    'key_file': None,  # No certificates for development
    'cert_file': None,  # No certificates for development
    'encryption_keypairs': [],
    'valid_for': 24,  # How long, in hours, metadata is valid
    'metadata': {
        'local': [],
        'remote': [
            {
                'url': 'https://metadata.surfconext.nl/entities',
                'cert': None,
            },
        ],
    },
}

# SAML Settings
SAML_ATTRIBUTE_MAPPING = {
    'uid': ('username',),
    'mail': ('email',),
    'cn': ('first_name',),
    'sn': ('last_name',),
    'schacHomeOrganization': ('university',),
    'schacPersonalUniqueCode': ('student_id',),
    'displayName': ('display_name',),
    'givenName': ('first_name',),
    'surname': ('last_name',),
}

# SAML Session Settings
SAML_SESSION_COOKIE_NAME = 'saml_session'
SAML_SESSION_COOKIE_AGE = 3600  # 1 hour
SAML_SESSION_COOKIE_SECURE = False  # Set to True in production
SAML_SESSION_COOKIE_HTTPONLY = True
SAML_SESSION_COOKIE_SAMESITE = 'Lax'

# SAML Logout Settings
SAML_LOGOUT_REQUEST_PREFERRED_BINDING = 'urn:oasis:names:tc:SAML:2.0:bindings:HTTP-Redirect'
SAML_LOGOUT_RESPONSE_PREFERRED_BINDING = 'urn:oasis:names:tc:SAML:2.0:bindings:HTTP-POST'

# SAML Security Settings
SAML_CSP_HANDLER = ''  # Disable CSP warnings for development
SAML_STRICT = True
SAML_DEBUG = settings.DEBUG 