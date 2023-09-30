from enum import Enum
from typing import Optional, Any, List, TypeVar, Type, cast, Callable


T = TypeVar("T")
EnumT = TypeVar("EnumT", bound=Enum)


def from_str(x: Any) -> str:
    assert isinstance(x, str)
    return x


def from_bool(x: Any) -> bool:
    assert isinstance(x, bool)
    return x


def from_none(x: Any) -> Any:
    assert x is None
    return x


def from_union(fs, x):
    for f in fs:
        try:
            return f(x)
        except:
            pass
    assert False


def to_enum(c: Type[EnumT], x: Any) -> EnumT:
    assert isinstance(x, c)
    return x.value


def from_int(x: Any) -> int:
    assert isinstance(x, int) and not isinstance(x, bool)
    return x


def to_class(c: Type[T], x: Any) -> dict:
    assert isinstance(x, c)
    return cast(Any, x).to_dict()


def from_list(f: Callable[[Any], T], x: Any) -> List[T]:
    assert isinstance(x, list)
    return [f(y) for y in x]


class OrganizationEnum(Enum):
    LUCASASANTANA = "lucasasantana"


class Component:
    organization: OrganizationEnum
    key: str
    uuid: str
    enabled: bool
    qualifier: str
    name: str
    long_name: str
    path: Optional[str]

    def __init__(self, organization: OrganizationEnum, key: str, uuid: str, enabled: bool, qualifier: str, name: str, long_name: str, path: Optional[str]) -> None:
        self.organization = organization
        self.key = key
        self.uuid = uuid
        self.enabled = enabled
        self.qualifier = qualifier
        self.name = name
        self.long_name = long_name
        self.path = path

    @staticmethod
    def from_dict(obj: Any) -> 'Component':
        assert isinstance(obj, dict)
        organization = OrganizationEnum(obj.get("organization"))
        key = from_str(obj.get("key"))
        uuid = from_str(obj.get("uuid"))
        enabled = from_bool(obj.get("enabled"))
        qualifier = from_str(obj.get("qualifier"))
        name = from_str(obj.get("name"))
        long_name = from_str(obj.get("longName"))
        path = from_union([from_str, from_none], obj.get("path"))
        return Component(organization, key, uuid, enabled, qualifier, name, long_name, path)

    def to_dict(self) -> dict:
        result: dict = {}
        result["organization"] = to_enum(OrganizationEnum, self.organization)
        result["key"] = from_str(self.key)
        result["uuid"] = from_str(self.uuid)
        result["enabled"] = from_bool(self.enabled)
        result["qualifier"] = from_str(self.qualifier)
        result["name"] = from_str(self.name)
        result["longName"] = from_str(self.long_name)
        if self.path is not None:
            result["path"] = from_union([from_str, from_none], self.path)
        return result


class CleanCodeAttribute(Enum):
    CLEAR = "CLEAR"
    COMPLETE = "COMPLETE"
    CONVENTIONAL = "CONVENTIONAL"
    DISTINCT = "DISTINCT"
    FOCUSED = "FOCUSED"
    FORMATTED = "FORMATTED"
    IDENTIFIABLE = "IDENTIFIABLE"
    LOGICAL = "LOGICAL"


class CleanCodeAttributeCategory(Enum):
    ADAPTABLE = "ADAPTABLE"
    CONSISTENT = "CONSISTENT"
    INTENTIONAL = "INTENTIONAL"


class EDate(Enum):
    THE_20230911_T22_58550200 = "2023-09-11T22:58:55+0200"
    THE_20230919_T02_35300200 = "2023-09-19T02:35:30+0200"


class Debt(Enum):
    THE_0_MIN = "0min"
    THE_10_MIN = "10min"
    THE_11_MIN = "11min"
    THE_13_MIN = "13min"
    THE_14_MIN = "14min"
    THE_15_MIN = "15min"
    THE_18_MIN = "18min"
    THE_1_MIN = "1min"
    THE_20_MIN = "20min"
    THE_23_MIN = "23min"
    THE_26_MIN = "26min"
    THE_2_H25_MIN = "2h25min"
    THE_2_MIN = "2min"
    THE_30_MIN = "30min"
    THE_43_MIN = "43min"
    THE_5_MIN = "5min"
    THE_6_MIN = "6min"
    THE_7_MIN = "7min"
    THE_8_MIN = "8min"


class Msg(Enum):
    DUPLICATION = "Duplication"
    ORIGINAL_IMPLEMENTATION = "original implementation"
    SHADOWED_FIELD = "Shadowed field."
    THE_1 = "+1"
    THE_2_INCL_1_FOR_NESTING = "+2 (incl. 1 for nesting)"
    THE_3_INCL_2_FOR_NESTING = "+3 (incl. 2 for nesting)"
    THE_4_INCL_3_FOR_NESTING = "+4 (incl. 3 for nesting)"
    THE_5_INCL_4_FOR_NESTING = "+5 (incl. 4 for nesting)"
    THE_6_INCL_5_FOR_NESTING = "+6 (incl. 5 for nesting)"


class TextRange:
    start_line: int
    end_line: int
    start_offset: int
    end_offset: int

    def __init__(self, start_line: int, end_line: int, start_offset: int, end_offset: int) -> None:
        self.start_line = start_line
        self.end_line = end_line
        self.start_offset = start_offset
        self.end_offset = end_offset

    @staticmethod
    def from_dict(obj: Any) -> 'TextRange':
        assert isinstance(obj, dict)
        start_line = from_int(obj.get("startLine"))
        end_line = from_int(obj.get("endLine"))
        start_offset = from_int(obj.get("startOffset"))
        end_offset = from_int(obj.get("endOffset"))
        return TextRange(start_line, end_line, start_offset, end_offset)

    def to_dict(self) -> dict:
        result: dict = {}
        result["startLine"] = from_int(self.start_line)
        result["endLine"] = from_int(self.end_line)
        result["startOffset"] = from_int(self.start_offset)
        result["endOffset"] = from_int(self.end_offset)
        return result


class Location:
    component: str
    text_range: TextRange
    msg: Optional[Msg]

    def __init__(self, component: str, text_range: TextRange, msg: Optional[Msg]) -> None:
        self.component = component
        self.text_range = text_range
        self.msg = msg

    @staticmethod
    def from_dict(obj: Any) -> 'Location':
        assert isinstance(obj, dict)
        component = from_str(obj.get("component"))
        text_range = TextRange.from_dict(obj.get("textRange"))
        msg = from_union([Msg, from_none], obj.get("msg"))
        return Location(component, text_range, msg)

    def to_dict(self) -> dict:
        result: dict = {}
        result["component"] = from_str(self.component)
        result["textRange"] = to_class(TextRange, self.text_range)
        if self.msg is not None:
            result["msg"] = from_union([lambda x: to_enum(Msg, x), from_none], self.msg)
        return result


class Flow:
    locations: List[Location]

    def __init__(self, locations: List[Location]) -> None:
        self.locations = locations

    @staticmethod
    def from_dict(obj: Any) -> 'Flow':
        assert isinstance(obj, dict)
        locations = from_list(Location.from_dict, obj.get("locations"))
        return Flow(locations)

    def to_dict(self) -> dict:
        result: dict = {}
        result["locations"] = from_list(lambda x: to_class(Location, x), self.locations)
        return result


class ImpactSeverity(Enum):
    HIGH = "HIGH"
    LOW = "LOW"
    MEDIUM = "MEDIUM"


class SoftwareQuality(Enum):
    MAINTAINABILITY = "MAINTAINABILITY"


class Impact:
    software_quality: SoftwareQuality
    severity: ImpactSeverity

    def __init__(self, software_quality: SoftwareQuality, severity: ImpactSeverity) -> None:
        self.software_quality = software_quality
        self.severity = severity

    @staticmethod
    def from_dict(obj: Any) -> 'Impact':
        assert isinstance(obj, dict)
        software_quality = SoftwareQuality(obj.get("softwareQuality"))
        severity = ImpactSeverity(obj.get("severity"))
        return Impact(software_quality, severity)

    def to_dict(self) -> dict:
        result: dict = {}
        result["softwareQuality"] = to_enum(SoftwareQuality, self.software_quality)
        result["severity"] = to_enum(ImpactSeverity, self.severity)
        return result


class Project(Enum):
    LUCASASANTANA_FIREFOX_IOS = "lucasasantana_firefox-ios"


class Resolution(Enum):
    FIXED = "FIXED"


class IssueSeverity(Enum):
    BLOCKER = "BLOCKER"
    CRITICAL = "CRITICAL"
    INFO = "INFO"
    MAJOR = "MAJOR"
    MINOR = "MINOR"


class Status(Enum):
    CLOSED = "CLOSED"
    OPEN = "OPEN"


class Tag(Enum):
    BAD_PRACTICE = "bad-practice"
    BRAIN_OVERLOAD = "brain-overload"
    CLUMSY = "clumsy"
    CONFUSING = "confusing"
    CONVENTION = "convention"
    CWE = "cwe"
    DESIGN = "design"
    DUPLICATE = "duplicate"
    PITFALL = "pitfall"
    REDUNDANT = "redundant"
    SUSPICIOUS = "suspicious"
    UNUSED = "unused"


class TypeEnum(Enum):
    CODE_SMELL = "CODE_SMELL"


class Issue:
    key: str
    rule: str
    severity: IssueSeverity
    component: str
    project: Project
    line: Optional[int]
    hash: str
    text_range: TextRange
    flows: List[Flow]
    status: Status
    message: str
    effort: Debt
    debt: Debt
    author: str
    tags: List[Tag]
    creation_date: str
    update_date: EDate
    type: TypeEnum
    organization: OrganizationEnum
    clean_code_attribute: CleanCodeAttribute
    clean_code_attribute_category: CleanCodeAttributeCategory
    impacts: List[Impact]
    resolution: Optional[Resolution]
    close_date: Optional[EDate]

    def __init__(self, key: str, rule: str, severity: IssueSeverity, component: str, project: Project, line: Optional[int], hash: str, text_range: TextRange, flows: List[Flow], status: Status, message: str, effort: Debt, debt: Debt, author: str, tags: List[Tag], creation_date: str, update_date: EDate, type: TypeEnum, organization: OrganizationEnum, clean_code_attribute: CleanCodeAttribute, clean_code_attribute_category: CleanCodeAttributeCategory, impacts: List[Impact], resolution: Optional[Resolution], close_date: Optional[EDate]) -> None:
        self.key = key
        self.rule = rule
        self.severity = severity
        self.component = component
        self.project = project
        self.line = line
        self.hash = hash
        self.text_range = text_range
        self.flows = flows
        self.status = status
        self.message = message
        self.effort = effort
        self.debt = debt
        self.author = author
        self.tags = tags
        self.creation_date = creation_date
        self.update_date = update_date
        self.type = type
        self.organization = organization
        self.clean_code_attribute = clean_code_attribute
        self.clean_code_attribute_category = clean_code_attribute_category
        self.impacts = impacts
        self.resolution = resolution
        self.close_date = close_date

    @staticmethod
    def from_dict(obj: Any) -> 'Issue':
        assert isinstance(obj, dict)
        key = from_str(obj.get("key"))
        rule = from_str(obj.get("rule"))
        severity = IssueSeverity(obj.get("severity"))
        component = from_str(obj.get("component"))
        project = Project(obj.get("project"))
        line = from_union([from_int, from_none], obj.get("line"))
        hash = from_str(obj.get("hash"))
        text_range = TextRange.from_dict(obj.get("textRange"))
        flows = from_list(Flow.from_dict, obj.get("flows"))
        status = Status(obj.get("status"))
        message = from_str(obj.get("message"))
        effort = Debt(obj.get("effort"))
        debt = Debt(obj.get("debt"))
        author = from_str(obj.get("author"))
        tags = from_list(Tag, obj.get("tags"))
        creation_date = from_str(obj.get("creationDate"))
        update_date = EDate(obj.get("updateDate"))
        type = TypeEnum(obj.get("type"))
        organization = OrganizationEnum(obj.get("organization"))
        clean_code_attribute = CleanCodeAttribute(obj.get("cleanCodeAttribute"))
        clean_code_attribute_category = CleanCodeAttributeCategory(obj.get("cleanCodeAttributeCategory"))
        impacts = from_list(Impact.from_dict, obj.get("impacts"))
        resolution = from_union([Resolution, from_none], obj.get("resolution"))
        close_date = from_union([EDate, from_none], obj.get("closeDate"))
        return Issue(key, rule, severity, component, project, line, hash, text_range, flows, status, message, effort, debt, author, tags, creation_date, update_date, type, organization, clean_code_attribute, clean_code_attribute_category, impacts, resolution, close_date)

    def to_dict(self) -> dict:
        result: dict = {}
        result["key"] = from_str(self.key)
        result["rule"] = from_str(self.rule)
        result["severity"] = to_enum(IssueSeverity, self.severity)
        result["component"] = from_str(self.component)
        result["project"] = to_enum(Project, self.project)
        if self.line is not None:
            result["line"] = from_union([from_int, from_none], self.line)
        result["hash"] = from_str(self.hash)
        result["textRange"] = to_class(TextRange, self.text_range)
        result["flows"] = from_list(lambda x: to_class(Flow, x), self.flows)
        result["status"] = to_enum(Status, self.status)
        result["message"] = from_str(self.message)
        result["effort"] = to_enum(Debt, self.effort)
        result["debt"] = to_enum(Debt, self.debt)
        result["author"] = from_str(self.author)
        result["tags"] = from_list(lambda x: to_enum(Tag, x), self.tags)
        result["creationDate"] = from_str(self.creation_date)
        result["updateDate"] = to_enum(EDate, self.update_date)
        result["type"] = to_enum(TypeEnum, self.type)
        result["organization"] = to_enum(OrganizationEnum, self.organization)
        result["cleanCodeAttribute"] = to_enum(CleanCodeAttribute, self.clean_code_attribute)
        result["cleanCodeAttributeCategory"] = to_enum(CleanCodeAttributeCategory, self.clean_code_attribute_category)
        result["impacts"] = from_list(lambda x: to_class(Impact, x), self.impacts)
        if self.resolution is not None:
            result["resolution"] = from_union([lambda x: to_enum(Resolution, x), from_none], self.resolution)
        if self.close_date is not None:
            result["closeDate"] = from_union([lambda x: to_enum(EDate, x), from_none], self.close_date)
        return result


class OrganizationElement:
    key: OrganizationEnum
    name: str

    def __init__(self, key: OrganizationEnum, name: str) -> None:
        self.key = key
        self.name = name

    @staticmethod
    def from_dict(obj: Any) -> 'OrganizationElement':
        assert isinstance(obj, dict)
        key = OrganizationEnum(obj.get("key"))
        name = from_str(obj.get("name"))
        return OrganizationElement(key, name)

    def to_dict(self) -> dict:
        result: dict = {}
        result["key"] = to_enum(OrganizationEnum, self.key)
        result["name"] = from_str(self.name)
        return result


class Paging:
    page_index: int
    page_size: int
    total: int

    def __init__(self, page_index: int, page_size: int, total: int) -> None:
        self.page_index = page_index
        self.page_size = page_size
        self.total = total

    @staticmethod
    def from_dict(obj: Any) -> 'Paging':
        assert isinstance(obj, dict)
        page_index = from_int(obj.get("pageIndex"))
        page_size = from_int(obj.get("pageSize"))
        total = from_int(obj.get("total"))
        return Paging(page_index, page_size, total)

    def to_dict(self) -> dict:
        result: dict = {}
        result["pageIndex"] = from_int(self.page_index)
        result["pageSize"] = from_int(self.page_size)
        result["total"] = from_int(self.total)
        return result


class Issues:
    total: int
    p: int
    ps: int
    paging: Paging
    effort_total: int
    debt_total: int
    issues: List[Issue]
    components: List[Component]
    organizations: List[OrganizationElement]
    facets: List[Any]

    def __init__(self, total: int, p: int, ps: int, paging: Paging, effort_total: int, debt_total: int, issues: List[Issue], components: List[Component], organizations: List[OrganizationElement], facets: List[Any]) -> None:
        self.total = total
        self.p = p
        self.ps = ps
        self.paging = paging
        self.effort_total = effort_total
        self.debt_total = debt_total
        self.issues = issues
        self.components = components
        self.organizations = organizations
        self.facets = facets

    @staticmethod
    def from_dict(obj: Any) -> 'Issues':
        assert isinstance(obj, dict)
        total = from_int(obj.get("total"))
        p = from_int(obj.get("p"))
        ps = from_int(obj.get("ps"))
        paging = Paging.from_dict(obj.get("paging"))
        effort_total = from_int(obj.get("effortTotal"))
        debt_total = from_int(obj.get("debtTotal"))
        issues = from_list(Issue.from_dict, obj.get("issues"))
        components = from_list(Component.from_dict, obj.get("components"))
        organizations = from_list(OrganizationElement.from_dict, obj.get("organizations"))
        facets = from_list(lambda x: x, obj.get("facets"))
        return Issues(total, p, ps, paging, effort_total, debt_total, issues, components, organizations, facets)

    def to_dict(self) -> dict:
        result: dict = {}
        result["total"] = from_int(self.total)
        result["p"] = from_int(self.p)
        result["ps"] = from_int(self.ps)
        result["paging"] = to_class(Paging, self.paging)
        result["effortTotal"] = from_int(self.effort_total)
        result["debtTotal"] = from_int(self.debt_total)
        result["issues"] = from_list(lambda x: to_class(Issue, x), self.issues)
        result["components"] = from_list(lambda x: to_class(Component, x), self.components)
        result["organizations"] = from_list(lambda x: to_class(OrganizationElement, x), self.organizations)
        result["facets"] = from_list(lambda x: x, self.facets)
        return result


def issues_from_dict(s: Any) -> Issues:
    return Issues.from_dict(s)


def issues_to_dict(x: Issues) -> Any:
    return to_class(Issues, x)
