from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, Field

class EvaluateRequest(BaseModel):
    marka: str = Literal[
        "Mercedes-Benz", "SsangYong", "Alfa Romeo", "BMW", "Alpina", "DS Automobiles", "Land Rover", "Lynk & Co", "Aston Martin", "Lada", "Buick", "Chatenet", "UAZ", "Renault", "Volvo", "Hyundai", "Ford", "Opel", "Mazda", "Volkswagen", "Audi", "Nissan", "Skoda", "Toyota", "Kia", "Suzuki", "Jaguar", "Citroen", "Infiniti", "Honda", "Seat", "Dacia", "Jeep", "Chevrolet", "MG", "Fiat", "MINI", "Maserati", "Porsche", "Peugeot", "Cupra", "Lexus", "Dodge", "BAIC", "Mitsubishi", "Tesla", "RAM", "Chrysler", "Daewoo", "Omoda", "Subaru", "BYD", "Daihatsu", "Leapmotor", "Lancia", "Smart", "Maxus", "Jaecoo", "Abarth", "Pontiac", "SARINI", "Microcar", "Cadillac", "Lamborghini", "GMC", "Bentley", "Saab", "Rolls-Royce", "MAN", "Chery", "Aixam", "Ferrari", "Polonez", "Genesis", "Vanderhall", "Iveco", "Mercury", "Acura", "Lincoln", "Alpine", "Hummer", "Oldsmobile", "Warszawa", "DFSK", "Ligier", "Geely", "Trabant", "Aito", "BAW", "Rover", "McLaren", "JAC", "Lotus", "Corvette", "Hongqi", "XPENG", "Isuzu", "Forthing", "Cenntro", "Microlino", "Wartburg", "GWM", "Bestune", "Zhidou", "DKW", "Wołga", "Dongfeng", "Morgan", "Brilliance", "Xiaomi", "GAC", "Voyah", "Santana", "Ineos", "LTI", "Denza", "Tata", "Li", "Nysa", "Wiesmann", "Plymouth", "Gaz", "Polestar", "FOTON", "Seres", "Austin", "e.GO", "Skywell", "Syrena", "Triumph", "Saturn", "DeLorean", "Piaggio", "Asia", "Jetour", "Fisker", "Tarpan", "Jinpeng", "Skyworth", "AVATR", "FAW", "Zastava", "ZEEKR", "Biro", "Żuk", "Vauxhall", "SWM", "NSU", "ORA", "Barkas", "Casalini", "Borgward", "Changan", "WEY", "Lixiang", "Bugatti", "LEVC", "Ariel", "Bentu", "KTM", "Cobra", "DeTomaso", "Lucid", "Riley", "XEV", "NIO", "Delahaye", "Caterham", "Silence", "Donkervoort", "DR MOTOR", "Sportequipe", "Aiways", "ICH-X", "Artega", "TECHART", "Elaris", "Charge", "Westfield", "TVR", "Datsun"
    ]
    moc_silnika: int = Field(..., ge=1, le=5000)
    przebieg: int = Field(..., ge=0, le=5_000_000)
    rodzaj_paliwa: Literal[
        "Benzyna",
        "Diesel",
        "Hybryda",
        "Elektryczny",
        "LPG",
    ]
    rok_produkcji: int = Field(..., ge=1886, le=2027)
    typ_skrzyni_biegow: Literal[
        "Manualna",
        "Automatyczna",
    ]

class ValuationResponse(BaseModel):
    price: int | None = None
    detail: str | None = None
    error: str | None = None
    message: str | None = None