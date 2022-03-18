from app.chat.organizations import BUKLOD, KADIWA, BINHI


class Group:
    def __init__(self) -> None:
        self.id: int = None
        self.program_name: str = None
        return


class GroupManager:
    def __init__(self) -> None:
        self.main_groups: dict[int, MainGroup] = dict()
        self.subgroups: dict[int, Subgroup] = dict()
        return

    def add_group(self, id: int, program_name: str) -> None:
        return

    def remove_group(self, id: int) -> None:
        return

    def find_group(self, id: int, program_name: str) -> Group:
        return


class MainGroup(Group):
    def __init__(self) -> None:
        self.subgroups: list[Subgroup] = list()
        self.total_area: int = 0
        self.total_locale_serial_number: int = 0
        self.total_organization_serial_number: dict[str, int] = {
            BUKLOD: 0,
            KADIWA: 0,
            BINHI: 0,
        }
        return

    def add_subgroup(self, id: int) -> None:
        return

    def remove_subgroup(self) -> None:
        return

    def update_locale_serial_number(
        self, old_serial_number: int, new_serial_number: int
    ) -> None:
        return

    def update_organization_serial_number(
        self, organization: str, old_serial_number: int, new_serial_number: int
    ) -> None:
        return


class Subgroup(Group):
    def __init__(self) -> None:
        self.parent_group: MainGroup = None
        self.area: int = None
        self.locale_serial_number: int = 0
        self.organization_serial_number: dict[str, int] = {
            BUKLOD: 0,
            KADIWA: 0,
            BINHI: 0,
        }
        return

    def set_locale_serial_number(self, serial_number: int) -> None:
        return

    def set_organization_serial_number(
        self, organization: str, serial_number: int
    ) -> None:
        return
