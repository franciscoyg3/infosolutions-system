class EmployeeModel:
    def __init__(self, name, position, base_salary, bonus=0, id=None):
        name, position = name.strip(), position.strip()
        if not name or not position:
            raise ValueError("Empty values are not allowed.")
        if base_salary < 0 or bonus < 0:
            raise ValueError("Salary and bonus cannot be negative.")

        self.id, self.name = id, name
        self.position, self.base_salary, self.bonus = position, base_salary, bonus

    @property
    def total_salary(self):
        return self.base_salary + self.bonus

    def add_employee(self, db):
        with db.connect() as con:
            cur = con.execute(
                "INSERT INTO employees (name, position, base_salary, bonus) VALUES (?,?,?,?)",
                (self.name, self.position, self.base_salary, self.bonus)
            )
            self.id = cur.lastrowid

    @staticmethod
    def remove_employee(db, id):
        with db.connect() as con:
            cur = con.execute(
                "DELETE FROM employees WHERE id=?", (id,)
            )
            if cur.rowcount == 0:
                raise ValueError("Employee not found.")

    @staticmethod
    def list_employees(db):
        with db.connect() as con:
            rows = con.execute(
                "SELECT id, name, position, base_salary, bonus FROM employees"
            ).fetchall()
        return [
            EmployeeModel(name, position, base_salary, bonus, id)
            for id, name, position, base_salary, bonus in rows
        ]

    @staticmethod
    def calculate_payroll(db):
        with db.connect() as con:
            result = con.execute(
                "SELECT COALESCE(SUM(base_salary + COALESCE(bonus, 0)), 0) FROM employees"
            ).fetchone()
        return result[0]

    @staticmethod
    def get_highest_paid(db):
        with db.connect() as con:
            rows = con.execute("""
                SELECT id, name, position, base_salary, COALESCE(bonus, 0)
                FROM employees
                WHERE base_salary + COALESCE(bonus, 0) = (
                    SELECT MAX(base_salary + COALESCE(bonus, 0)) FROM employees
                )
            """).fetchall()
        return [
            EmployeeModel(name, position, base_salary, bonus, id)
            for id, name, position, base_salary, bonus in rows
        ]