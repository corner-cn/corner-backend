class SpecialFlag(object):
    PRIORITY = "priority"
    CHECK_IN = "check-in"
    LATEST = "latest"
    NEARBY = "nearby"


class QueryType(object):
    RECOMMENDATION = "recommendation"
    KEYWORDS = "keywords"
    PRIORITY = "priority"
    COMBINED = "combined"


class QueryParams(object):
    KEYWORDS = "keywords"
    DISTANCE = "distance"
    CITY = "city"
    DISTRICT = "district"
    BUSINESS_DISTRICT = "business_district"
    ORDER_BY = "order_by"
    CATEGORY = "category"

class BoothOperation(object):
    CHECK_IN = "check_in"

