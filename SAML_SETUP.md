# SAML Authentication Setup for StudentZone

## Overview

StudentZone uses SAML 2.0 authentication through SurfConext to provide secure Single Sign-On (SSO) for Dutch university students. This allows students to log in using their university credentials without creating separate accounts.

## Supported Universities

StudentZone supports authentication for students from all major Dutch educational institutions:

### Research Universities (WO)
- **TU Delft** (`tudelft.nl`) - Delft University of Technology
- **University of Amsterdam** (`uva.nl`) - UvA
- **Utrecht University** (`uu.nl`) - UU
- **Eindhoven University of Technology** (`tue.nl`) - TU/e
- **Wageningen University & Research** (`wur.nl`) - WUR
- **Radboud University** (`ru.nl`) - Radboud
- **Vrije Universiteit Amsterdam** (`vu.nl`) - VU
- **Leiden University** (`leidenuniv.nl`) - Leiden
- **University of Groningen** (`rug.nl`) - RUG
- **Maastricht University** (`maastrichtuniversity.nl`) - UM
- **Tilburg University** (`tilburguniversity.edu`) - TiU
- **Open University** (`ou.nl`) - OU

### Universities of Applied Sciences (HBO)
- **Fontys University of Applied Sciences** (`fontys.nl`)
- **HAN University of Applied Sciences** (`han.nl`)
- **Amsterdam University of Applied Sciences** (`hva.nl`) - HvA
- **Rotterdam University of Applied Sciences** (`hr.nl`) - HR
- **Utrecht University of Applied Sciences** (`hu.nl`) - HU
- **Windesheim University of Applied Sciences** (`windesheim.nl`)
- **Avans University of Applied Sciences** (`avans.nl`)
- **Inholland University of Applied Sciences** (`inholland.nl`)
- **Saxion University of Applied Sciences** (`saxion.nl`)
- **NHL Stenden University of Applied Sciences** (`nhlstenden.com`)
- **HZ University of Applied Sciences** (`hz.nl`)
- **Zuyd University of Applied Sciences** (`zuyd.nl`)
- **The Hague University of Applied Sciences** (`hsleiden.nl`)
- **Rotterdam University of Applied Sciences** (`hsrotterdam.nl`)
- **Amsterdam University of Applied Sciences** (`hsamsterdam.nl`)
- **Utrecht University of Applied Sciences** (`hsutrecht.nl`)
- **Eindhoven University of Applied Sciences** (`hseindhoven.nl`)
- **Tilburg University of Applied Sciences** (`hstilburg.nl`)
- **Breda University of Applied Sciences** (`hsbreda.nl`)
- **Arnhem and Nijmegen University of Applied Sciences** (`hsarnhem.nl`)
- **Groningen University of Applied Sciences** (`hsgroningen.nl`)
- **Leeuwarden University of Applied Sciences** (`hsleeuwarden.nl`)
- **Zwolle University of Applied Sciences** (`hszwolle.nl`)

### Universities of the Arts
- **ArtEZ University of the Arts** (`artez.nl`)
- **Amsterdam University of the Arts** (`ahk.nl`) - AHK
- **Codarts University of the Arts** (`codarts.nl`)
- **Conservatorium van Amsterdam** (`conservatoriumvanamsterdam.nl`)
- **Design Academy Eindhoven** (`designacademy.nl`)
- **Gerrit Rietveld Academie** (`gerritrietveldacademie.nl`)
- **Royal Academy of Art, The Hague** (`kabk.nl`) - KABK
- **Royal Conservatoire The Hague** (`royalconservatoire.nl`)
- **Utrecht Conservatory** (`utrechtconservatory.nl`)
- **Willem de Kooning Academy** (`wdka.nl`)

### Medical Centers
- **Erasmus University Medical Center** (`erasmusmc.nl`)
- **Academic Medical Center Amsterdam** (`amc.nl`)
- **University Medical Center Utrecht** (`umcutrecht.nl`)
- **Leiden University Medical Center** (`lumc.nl`)
- **University Medical Center Groningen** (`umcg.nl`)
- **Maastricht University Medical Center** (`mumc.nl`)
- **Radboud University Medical Center** (`radboudumc.nl`)
- **VU University Medical Center** (`vumc.nl`)

## Components

### 1. SAML Configuration (`studentzone/settings.py`)
- **Service Provider (SP)**: StudentZone acts as the SP
- **Entity ID**: `http://127.0.0.1:8000/saml2/metadata/` (development)
- **Endpoints**: ACS and SLO endpoints configured
- **Attribute Mapping**: Maps SAML attributes to Django User model fields

### 2. Custom SAML Backend (`core/saml_backend.py`)
- **SurfConextSaml2Backend**: Handles user creation and attribute mapping
- **University Mapping**: Maps university codes to full names
- **Profile Creation**: Automatically creates UserProfile instances
- **Student ID Mapping**: Maps `schacPersonalUniqueCode` to student_id

### 3. Attribute Mapping
SAML attributes are mapped to Django User model fields:

| SAML Attribute | Django Field | Description |
|----------------|--------------|-------------|
| `uid` | `username` | Unique identifier |
| `mail` | `email` | Email address |
| `cn` | `first_name` | Common name (first name) |
| `sn` | `last_name` | Surname (last name) |
| `schacHomeOrganization` | `university` | University code |
| `schacPersonalUniqueCode` | `student_id` | Student ID number |

## Development Setup

### 1. Install Dependencies
```bash
pip install djangosaml2==1.5.9 pysaml2==9.0.0 cryptography==41.0.7
brew install xmlsec1  # macOS
```

### 2. Generate SSL Certificates (Optional)
```bash
python manage.py generate_saml_certs
```

### 3. Test SAML Configuration
- Visit `/saml/test/` to check configuration status
- Use `/dev/login/` for development testing without real IdP
- Test metadata generation at `/saml2/metadata/`

### 4. Development Login Simulation
The development login form (`/dev/login/`) allows testing with:
- All supported Dutch universities
- Custom student information
- Automatic user and profile creation
- Real university mapping

## Production Setup

### 1. Register with SurfConext
1. Contact SurfConext for SP registration
2. Provide metadata URL: `https://yourdomain.com/saml2/metadata/`
3. Configure attribute release policies
4. Set up proper SSL certificates

### 2. Update Configuration
```python
# Update entity ID and endpoints
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
}
```

### 3. Security Settings
```python
# Enable security for production
SAML_CONFIG['service']['sp']['authn_requests_signed'] = True
SAML_CONFIG['service']['sp']['want_assertions_signed'] = True
SAML_CONFIG['service']['sp']['want_response_signed'] = True
SAML_CONFIG['service']['sp']['want_assertions_or_response_signed'] = True
SAML_CONFIG['service']['sp']['want_digest'] = True
SAML_CONFIG['service']['sp']['want_signature_validation'] = True
```

## User Flow

1. **Student clicks "Sign in with your University"**
2. **Redirected to SurfConext** with university selection
3. **Student selects their university** and enters credentials
4. **SurfConext authenticates** and sends SAML assertion
5. **StudentZone processes assertion** and creates/updates user
6. **Student is logged in** with their university profile

## Troubleshooting

### Common Issues

1. **IdPConfigurationMissing**: No Identity Provider configured
   - **Solution**: Add proper IdP configuration or use development login

2. **SigverError**: Missing xmlsec1
   - **Solution**: Install xmlsec1: `brew install xmlsec1`

3. **SourceNotFound**: Remote metadata not accessible
   - **Solution**: Remove remote metadata for development

4. **UserProfile TypeError**: Missing student_id field
   - **Solution**: Run migrations: `python manage.py makemigrations core && python manage.py migrate`

### Debug Commands
```bash
# Test metadata generation
curl -s http://127.0.0.1:8000/saml2/metadata/

# Test development login
curl -s http://127.0.0.1:8000/dev/login/

# Check SAML status
curl -s http://127.0.0.1:8000/saml/test/
```

## Security Considerations

1. **HTTPS Required**: All SAML communication must use HTTPS in production
2. **Certificate Management**: Proper SSL certificate setup required
3. **Attribute Privacy**: Only request necessary attributes from IdP
4. **Session Management**: Implement proper session timeout and logout
5. **Audit Logging**: Log authentication events for security monitoring

## Future Enhancements

1. **Additional Universities**: Support for more international universities
2. **Role-based Access**: Different permissions based on university/role
3. **Multi-factor Authentication**: Additional security layers
4. **Attribute-based Authorization**: Fine-grained access control
5. **Federation Support**: Support for other identity federations 