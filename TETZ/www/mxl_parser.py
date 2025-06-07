import re
from typing import Dict, List


class MxlParser:
    @staticmethod
    def parse(mxl_content: str) -> Dict:
        """Расширенный парсер MXL-файлов 1С"""

        def clean_number(num_str: str) -> int:
            """Очищает число от форматирования"""
            try:
                return int(num_str.replace('\u00a0', '').replace(' ', ''))
            except:
                return 0

        result = {
            'metadata': {},
            'components': [],
            'complectation_status': {}
        }

        # Парсинг метаданных
        if header := re.search(r'\{"#","(.+?)"\}', mxl_content):
            result['metadata']['title'] = header.group(1)
            if date := re.search(r'на (\d{2}\.\d{2}\.\d{4})', header.group(1)):
                result['metadata']['date'] = date.group(1)

        # Парсинг компонентов
        component_pattern = re.compile(
            r'\{"#","(.+?)"\}.*?'  # Наименование
            r'\{"#","(.+?)"\}.*?'  # Требуется
            r'\{"#","(.+?)"\}'  # Доступно
        )

        for match in component_pattern.finditer(mxl_content):
            name, req, avail = match.groups()
            req_num = clean_number(req)
            avail_num = clean_number(avail)

            result['components'].append({
                'component': name,
                'required': req_num,
                'available': avail_num,
                'deficit': max(0, req_num - avail_num)
            })

        # Парсинг статуса комплектации
        status_pattern = re.compile(
            r'\{"#","(.+?)%"\}.*?'  # Укомплектовано
            r'\{"#","(.+?)%"\}.*?'  # Частично
            r'\{"#","(.+?)%"\}'  # Отсутствует
        )

        if status_match := status_pattern.search(mxl_content):
            result['complectation_status'] = {
                'completed': status_match.group(1),
                'partial': status_match.group(2),
                'missing': status_match.group(3)
            }

        return result