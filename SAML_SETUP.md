# SAML Authentication Setup for StudentZone

This document explains how to set up SAML authentication with SurfConext for StudentZone.

## Overview

StudentZone uses SAML (Security Assertion Markup Language) to authenticate users through their university credentials via SurfConext. This provides:

- **Secure Authentication**: Users log in with their university credentials
- **Automatic User Creation**: New users are created automatically from SAML attributes
- **University Integration**: Users are automatically associated with their university
- **Single Sign-On**: Users can access multiple services with one login

## Components

### 1. SAML Configuration (`saml_config.py`)

The main SAML configuration file contains:
- Service Provider (SP) settings
- Attribute mapping from SurfConext to Django user fields
- Metadata configuration for SurfConext
- Security settings

### 2. Custom SAML Backend (`core/saml_backend.py`)

Handles:
- User creation from SAML attributes
- University mapping from `schacHomeOrganization`
- Student ID extraction from `schacPersonalUniqueCode`
- Profile creation and updates

### 3. Attribute Mapping

SurfConext provides these attributes:
- `uid` → `username`
- `mail` → `email`
- `cn` → `first_name`
- `sn` → `last_name`
- `schacHomeOrganization` → `university`
- `schacPersonalUniqueCode` → `student_id`

## Development Setup

### 1. Install Dependencies

```bash
pip install djangosaml2 pysaml2 cryptography
```

### 2. Generate Certificates (Optional)

For development, you can generate self-signed certificates:

```bash
python manage.py generate_saml_certs
```

### 3. Test the Setup

Visit `/saml/test/` to see the SAML configuration status.

## Production Setup

### 1. Register with SurfConext

1. Contact SurfConext to register your service
2. Provide your metadata URL: `https://yourdomain.com/saml2/metadata/`
3. Receive your entity ID and configuration

### 2. Update Configuration

Update `saml_config.py` with production settings:

```python
SAML_CONFIG = {
    'entityid': 'https://yourdomain.com/saml2/metadata/',
    'service': {
        'sp': {
            'endpoints': {
                'assertion_consumer_service': [
                    ('https://yourdomain.com/saml2/acs/', 'urn:oasis:names:tc:SAML:2.0:bindings:HTTP-POST'),
                ],
                'single_logout_service': [
                    ('https://yourdomain.com/saml2/ls/', 'urn:oasis:names:tc:SAML:2.0:bindings:HTTP-Redirect'),
                ],
            },
        },
    },
    'key_file': '/path/to/your/private.key',
    'cert_file': '/path/to/your/certificate.crt',
}
```

### 3. Security Settings

For production, update these settings:

```python
SAML_SESSION_COOKIE_SECURE = True
SAML_STRICT = True
SAML_DEBUG = False
```

## Supported Universities

The system automatically maps these university codes:

- `tudelft.nl` → TU Delft
- `uva.nl` → University of Amsterdam
- `uu.nl` → Utrecht University
- `tue.nl` → Eindhoven University of Technology
- `wur.nl` → Wageningen University & Research
- `ru.nl` → Radboud University
- `vu.nl` → Vrije Universiteit Amsterdam
- `leidenuniv.nl` → Leiden University
- `rug.nl` → University of Groningen
- `maastrichtuniversity.nl` → Maastricht University
- And many more...

## User Flow

1. User clicks "Sign in with your University"
2. User is redirected to SurfConext
3. User selects their university
4. User authenticates with their university credentials
5. SurfConext sends SAML response to StudentZone
6. StudentZone creates/updates user account
7. User is logged in and redirected to home page

## Troubleshooting

### Common Issues

1. **CSP Warnings**: Set `SAML_CSP_HANDLER = ''` in development
2. **Certificate Issues**: Ensure certificates are properly generated and configured
3. **Attribute Mapping**: Check that SurfConext is sending expected attributes
4. **Metadata Issues**: Verify metadata URL is accessible

### Debug Mode

Enable debug mode to see detailed SAML information:

```python
SAML_DEBUG = True
```

### Testing

Use the test page at `/saml/test/` to verify:
- SAML configuration
- Metadata generation
- Login flow

## Security Considerations

- Always use HTTPS in production
- Keep private keys secure
- Regularly update certificates
- Monitor SAML logs for suspicious activity
- Implement proper session management

## Support

For issues with:
- **SurfConext**: Contact SurfConext support
- **SAML Configuration**: Check djangosaml2 documentation
- **StudentZone Integration**: Check this documentation 