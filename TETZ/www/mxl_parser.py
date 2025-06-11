import re
from typing import Dict, List


class MxlParser:
    @staticmethod
    def parse(mxl_content: str) -> Dict:
        """Парсер для MXL-файлов нового формата"""
        result = {
            'metadata': {},
            'components': [],
            'complectation_status': {}
        }

        # Разделяем файл на строки
        lines = [line.strip() for line in mxl_content.split('\n') if line.strip()]

        current_section = None

        for line in lines:
            # Определяем секции
            if line.startswith('{"') and '"}' in line:
                key_value = line[2:-2].split('","')
                if len(key_value) == 1:
                    # Это заголовок секции
                    current_section = key_value[0]
                    result['metadata'][current_section] = {}
                elif len(key_value) == 2:
                    key, value = key_value
                    if current_section:
                        # Добавляем в текущую секцию
                        if current_section not in result:
                            result[current_section] = {}
                        result[current_section][key] = value
                    else:
                        # Простое ключ-значение
                        result['metadata'][key] = value

        # Преобразуем данные в нужный формат
        if 'СТАТОР' in result:
            result['components'].append({
                'component': 'СТАТОР',
                'Укомплектован': result['СТАТОР'].get('Укомплектован', '0'),
                'Частично укомплектован': result['СТАТОР'].get('Частично укомплектован', '0'),
                'Нет в наличие': result['СТАТОР'].get('Нет в наличие', '0')
            })

        if 'УПАКОВКА на 2 изделия' in result:
            result['components'].append({
                'component': 'УПАКОВКА на 2 изделия',
                'Укомплектован': result['УПАКОВКА на 2 изделия'].get('Укомплектован', '0'),
                'Частично укомплектован': result['УПАКОВКА на 2 изделия'].get('Частично укомплектован', '0'),
                'Нет в наличие': result['УПАКОВКА на 2 изделия'].get('Нет в наличие', '0')
            })

        return result