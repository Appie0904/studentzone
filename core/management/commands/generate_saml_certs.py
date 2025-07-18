from django.core.management.base import BaseCommand
from django.conf import settings
import os
import subprocess
import tempfile


class Command(BaseCommand):
    help = 'Generate SAML certificates for testing SurfConext integration'

    def handle(self, *args, **options):
        self.stdout.write('Generating SAML certificates...')
        
        # Create certs directory
        certs_dir = os.path.join(settings.BASE_DIR, 'certs')
        os.makedirs(certs_dir, exist_ok=True)
        
        # Generate private key
        private_key_path = os.path.join(certs_dir, 'private.key')
        cert_path = os.path.join(certs_dir, 'certificate.crt')
        
        if not os.path.exists(private_key_path):
            self.stdout.write('Generating private key...')
            subprocess.run([
                'openssl', 'genrsa', '-out', private_key_path, '2048'
            ], check=True)
            self.stdout.write(self.style.SUCCESS('Private key generated'))
        
        if not os.path.exists(cert_path):
            self.stdout.write('Generating certificate...')
            # Create a temporary config file
            with tempfile.NamedTemporaryFile(mode='w', suffix='.cnf', delete=False) as f:
                f.write("""
[req]
distinguished_name = req_distinguished_name
req_extensions = v3_req
prompt = no

[req_distinguished_name]
C = NL
ST = Netherlands
L = Amsterdam
O = StudentZone
OU = Development
CN = studentzone.local

[v3_req]
keyUsage = keyEncipherment, dataEncipherment
extendedKeyUsage = serverAuth
subjectAltName = @alt_names

[alt_names]
DNS.1 = studentzone.local
DNS.2 = localhost
IP.1 = 127.0.0.1
""")
                config_path = f.name
            
            try:
                subprocess.run([
                    'openssl', 'req', '-new', '-x509', '-key', private_key_path,
                    '-out', cert_path, '-days', '365', '-config', config_path
                ], check=True)
                self.stdout.write(self.style.SUCCESS('Certificate generated'))
            finally:
                os.unlink(config_path)
        
        # Update settings
        self.stdout.write('Updating SAML configuration...')
        self._update_settings(private_key_path, cert_path)
        
        self.stdout.write(self.style.SUCCESS('SAML certificates generated successfully!'))
        self.stdout.write(f'Private key: {private_key_path}')
        self.stdout.write(f'Certificate: {cert_path}')
        self.stdout.write('Remember to update your SAML configuration in production!')

    def _update_settings(self, private_key_path, cert_path):
        """Update settings.py with certificate paths"""
        settings_file = os.path.join(settings.BASE_DIR, 'studentzone', 'settings.py')
        
        with open(settings_file, 'r') as f:
            content = f.read()
        
        # Update SAML_CONFIG
        content = content.replace(
            "'key_file': None,  # Path to private key file",
            f"'key_file': '{private_key_path}',  # Path to private key file"
        )
        content = content.replace(
            "'cert_file': None,  # Path to certificate file",
            f"'cert_file': '{cert_path}',  # Path to certificate file"
        )
        
        with open(settings_file, 'w') as f:
            f.write(content) 