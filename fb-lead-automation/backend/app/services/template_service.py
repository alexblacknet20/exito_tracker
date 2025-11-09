import re
from flask import current_app

class TemplateService:
    """Service for processing message templates"""

    def fill_template(self, template_text, lead_data, variables=None):
        """
        Fill template with lead data and custom variables

        Args:
            template_text: Template string with {{placeholders}}
            lead_data: Dictionary with lead form data
            variables: Dictionary with custom variables

        Returns:
            str: Filled template text
        """
        try:
            if not template_text:
                return ''

            filled_text = template_text
            variables = variables or {}

            # Find all placeholders
            placeholders = self.extract_placeholders(template_text)

            for placeholder in placeholders:
                # Try to replace from lead_data first
                value = lead_data.get(placeholder)

                # If not in lead_data, try variables
                if value is None:
                    value = variables.get(placeholder)

                # If still not found, leave placeholder or use empty string
                if value is None:
                    current_app.logger.warning(f'Placeholder {{{{{placeholder}}}}} not found in data or variables')
                    value = ''

                # Replace placeholder
                filled_text = filled_text.replace(f'{{{{{placeholder}}}}}', str(value))

            return filled_text

        except Exception as e:
            current_app.logger.error(f'Error filling template: {str(e)}')
            return template_text

    def extract_placeholders(self, template_text):
        """
        Extract all placeholders from template text

        Args:
            template_text: Template string with {{placeholders}}

        Returns:
            list: List of placeholder names
        """
        try:
            if not template_text:
                return []

            # Find all {{placeholder}} patterns
            pattern = r'\{\{(\w+)\}\}'
            matches = re.findall(pattern, template_text)

            # Return unique placeholders
            return list(set(matches))

        except Exception as e:
            current_app.logger.error(f'Error extracting placeholders: {str(e)}')
            return []
