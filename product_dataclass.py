from dataclasses import dataclass


@dataclass
class Part:
    id: str
    name: str
    in_stock: bool
    variant_id: int
    variant_price_raw: int
    variant_price_formatted: float
    attr_design_number: int
    attr_colour_id: int
    attr_del_channel: str
    attr_system_name: str
    img_url: str
