import pickle
from app.chat.organizations import BUKLOD, KADIWA, BINHI
from app.config import CONFIG
from app.configs import GROUP_PERSISTENCE_FILE


def _format_for_html(text: str) -> str:
    result = "&lt;" + text[1:-1] + "&gt;"
    return result


class GroupManager:
    def __init__(self) -> None:
        self.main_groups: dict[int, MainGroup] = dict()
        self.subgroups: dict[int, Subgroup] = dict()
        return

    def add_group(self, id: int, program_name: str):
        if id in self.main_groups or id in self.subgroups:
            return
        program_names = [
            main_group.program_name for main_group in self.main_groups.values()
        ]
        if program_name not in program_names:
            main_group = MainGroup(id, program_name)
            self.main_groups[id] = main_group
            return main_group
        main_group: MainGroup = self.find_group(None, program_name)
        subgroup = main_group.add_subgroup(id)
        self.subgroups[id] = subgroup
        return subgroup

    def remove_group(self, id: int) -> None:
        if id not in self.main_groups or id not in self.subgroups:
            return
        group = self.find_group(id)
        if isinstance(group, MainGroup):
            if group.area != group.parent_group.total_area:
                return
            group.parent_group.remove_subgroup()
            self.subgroups.pop(id)
            return
        max_area = group.total_area
        for counter in range(max_area):
            subgroup = group.remove_subgroup()
            self.subgroups.pop(subgroup.id)
        self.main_groups.pop(id)
        return

    def find_group(self, id: int, program_name: str = None):
        if program_name != None:
            for group in self.main_groups.values():
                if program_name == group.program_name:
                    return group
            return
        for group in self.main_groups.values():
            if group.id == id:
                return group
        for group in self.subgroups.values():
            if group.id == id:
                return group
        return


class Group:
    def __init__(self) -> None:
        self.id: int = None
        self.program_name: str = None
        return


class MainGroup(Group):
    def __init__(self, id: int, program_name: str) -> None:
        self.id = id
        self.program_name = program_name
        self.subgroups: list[Subgroup] = list()
        self.total_area: int = 0
        self.total_locale_serial_number: int = 0
        self.total_organization_serial_number: dict[str, int] = {
            BUKLOD: 0,
            KADIWA: 0,
            BINHI: 0,
        }
        return

    def __str__(self) -> str:
        result = (
            "<b>ABOUT GROUP</b>"
            "\n<b>Group ID:</b> <code>%s</code>"
            "\n<b>Group type:</b> %s"
            "\n<b>Dedicated program:</b> %s"
            "\n<b>Subgroups:</b> %s"
            "\n<b>Total area:</b> %s"
            "\n<b>Total locale serial number:</b> %s"
            "\n<b>Total organization serial number:</b> %s"
            % (
                self.id,
                _format_for_html(str(type(self))),
                self.program_name,
                list(map(_format_for_html, str(self.subgroups)[1:-1].split(", "))),
                self.total_area,
                self.total_locale_serial_number,
                self.total_organization_serial_number,
            )
        )
        return result

    def add_subgroup(self, id: int):
        program_name = self.program_name
        parent_group = self
        area = self.total_area + 1
        subgroup: Subgroup = Subgroup(id, program_name, parent_group, area)
        self.subgroups.append(subgroup)
        self.total_area += 1
        return subgroup

    def remove_subgroup(self):
        subgroup: Subgroup = self.subgroups.pop()
        self.total_area -= 1
        self.total_locale_serial_number -= subgroup.locale_serial_number
        for organization in self.total_organization_serial_number:
            self.total_organization_serial_number[
                organization
            ] -= subgroup.organization_serial_number[organization]
        return subgroup

    def update_locale_serial_number(
        self, old_serial_number: int, new_serial_number: int
    ) -> None:
        serial_number_difference = new_serial_number - old_serial_number
        self.total_locale_serial_number += serial_number_difference
        return

    def update_organization_serial_number(
        self, organization: str, old_serial_number: int, new_serial_number: int
    ) -> None:
        serial_number_difference = new_serial_number - old_serial_number
        self.total_organization_serial_number[organization] += serial_number_difference
        return


class Subgroup(Group):
    def __init__(
        self, id: int, program_name: str, parent_group: MainGroup, area: int
    ) -> None:
        self.id = id
        self.program_name = program_name
        self.parent_group: MainGroup = parent_group
        self.area: int = area
        self.locale_serial_number: int = 0
        self.organization_serial_number: dict[str, int] = {
            BUKLOD: 0,
            KADIWA: 0,
            BINHI: 0,
        }
        return

    def __str__(self) -> str:
        result = (
            "<b>ABOUT GROUP</b>"
            "\n<b>Group ID:</b> <code>%s</code>"
            "\n<b>Group type:</b> %s"
            "\n<b>Dedicated program:</b> %s"
            "\n<b>Area:</b> %s"
            "\n<b>Locale serial number:</b> %s"
            "\n<b>Organization serial number:</b> %s"
            % (
                self.id,
                _format_for_html(str(type(self))),
                self.program_name,
                self.area,
                self.locale_serial_number,
                self.organization_serial_number,
            )
        )
        return result

    def set_locale_serial_number(self, serial_number: int) -> None:
        old_serial_number = self.locale_serial_number
        new_serial_number = serial_number
        self.locale_serial_number = new_serial_number
        self.parent_group.update_locale_serial_number(
            old_serial_number, new_serial_number
        )
        return

    def set_organization_serial_number(
        self, organization: str, serial_number: int
    ) -> None:
        old_serial_number = self.locale_serial_number
        new_serial_number = serial_number
        self.organization_serial_number[organization] = new_serial_number
        self.parent_group.update_organization_serial_number(
            organization, old_serial_number, new_serial_number
        )
        return


def load_group_manager() -> GroupManager:
    with open(CONFIG[GROUP_PERSISTENCE_FILE], "rb") as stream:
        group_manager = pickle.load(stream)
    return group_manager


def save_group_manager(group_manager: GroupManager) -> None:
    with open(CONFIG[GROUP_PERSISTENCE_FILE], "wb") as stream:
        pickle.dump(group_manager, stream)
    return
