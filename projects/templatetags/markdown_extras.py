import markdown
from django import template
from django.utils.safestring import mark_safe
from django.utils.html import escape

register = template.Library()

@register.filter(name='markdown')
def markdown_filter(text):
    """
    Convert markdown text to HTML with security features.
    Only allows safe HTML tags and attributes.
    """
    if not text:
        return ""
    
    # Escape any existing HTML to prevent XSS
    text = escape(text)
    
    # Configure markdown with safe extensions
    md = markdown.Markdown(
        extensions=[
            'markdown.extensions.codehilite',  # Syntax highlighting
            'markdown.extensions.fenced_code',  # Fenced code blocks
            'markdown.extensions.tables',       # Tables
            'markdown.extensions.nl2br',        # Line breaks
            'markdown.extensions.sane_lists',   # Better list handling
        ],
        extension_configs={
            'markdown.extensions.codehilite': {
                'css_class': 'highlight',
                'use_pygments': False,  # Don't use Pygments for security
            }
        }
    )
    
    # Convert markdown to HTML
    html = md.convert(text)
    
    # Mark as safe since we've already escaped the input
    return mark_safe(html) 