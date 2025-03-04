class TimeManager:
    def __init__(self, start_year: int = 2024):
        self.current_year = start_year
        self.current_month = 1
        self.current_day = 1
        
    def advance_year(self):
        """Avanza el tiempo un año"""
        self.current_year += 1
        
    def advance_month(self):
        """Avanza el tiempo un mes"""
        self.current_month += 1
        if self.current_month > 12:
            self.current_month = 1
            self.advance_year()
            
    def advance_day(self):
        """Avanza el tiempo un día"""
        self.current_day += 1
        days_in_month = self._get_days_in_month()
        if self.current_day > days_in_month:
            self.current_day = 1
            self.advance_month()
            
    def _get_days_in_month(self) -> int:
        """Retorna el número de días en el mes actual"""
        days = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
        # Ajuste para años bisiestos
        if self.current_month == 2 and self._is_leap_year():
            return 29
        return days[self.current_month - 1]
    
    def _is_leap_year(self) -> bool:
        """Determina si el año actual es bisiesto"""
        year = self.current_year
        return year % 4 == 0 and (year % 100 != 0 or year % 400 == 0) 