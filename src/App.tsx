import React, {useState, useRef, useEffect} from 'react';
import {motion, AnimatePresence} from 'motion/react';
import {Car, AlertCircle, Search, ChevronDown} from 'lucide-react';
import {ValuationRequest, ValuationResponse} from './types';

interface SelectProps {
    name: string;
    value: string;
    options: string[];
    onChange: (e: any) => void;
}

function CustomSelect({name, value, options, onChange}: SelectProps) {
    const [isOpen, setIsOpen] = useState(false);
    const selectRef = useRef<HTMLDivElement>(null);

    useEffect(() => {
        const handleClickOutside = (event: MouseEvent) => {
            if (selectRef.current && !selectRef.current.contains(event.target as Node)) {
                setIsOpen(false);
            }
        };
        document.addEventListener('mousedown', handleClickOutside);
        return () => document.removeEventListener('mousedown', handleClickOutside);
    }, []);

    return (
        <div className="relative" ref={selectRef}>
            <div
                className="w-full px-4 py-3 bg-slate-50 border border-slate-200 rounded-xl focus-within:ring-2 focus-within:ring-slate-900/10 focus-within:border-slate-900 outline-none text-sm cursor-pointer flex items-center justify-between transition-all"
                onClick={() => setIsOpen(!isOpen)}
            >
                <span className="truncate">{value}</span>
                <ChevronDown className={`w-4 h-4 text-slate-400 transition-transform ${isOpen ? 'rotate-180' : ''}`}/>
            </div>

            <AnimatePresence>
                {isOpen && (
                    <motion.div
                        initial={{opacity: 0, y: -5}}
                        animate={{opacity: 1, y: 0}}
                        exit={{opacity: 0, y: -5}}
                        transition={{duration: 0.15}}
                        className="absolute z-50 w-full mt-2 bg-white border border-slate-100 rounded-xl shadow-xl shadow-slate-200/50 overflow-y-auto max-h-60 py-1"
                    >
                        {options.map((option) => (
                            <div
                                key={option}
                                className={`px-4 py-2.5 text-sm cursor-pointer transition-colors max-w-full truncate ${
                                    value === option
                                        ? 'bg-slate-900 text-white font-semibold'
                                        : 'text-slate-600 hover:bg-slate-50 hover:text-slate-900'
                                }`}
                                onClick={() => {
                                    onChange({target: {name, value: option}});
                                    setIsOpen(false);
                                }}
                            >
                                {option}
                            </div>
                        ))}
                    </motion.div>
                )}
            </AnimatePresence>
        </div>
    );
}

const CAR_BRANDS = [
    "Mercedes-Benz", "SsangYong", "Alfa Romeo", "BMW", "Alpina", "DS Automobiles", "Land Rover", "Lynk & Co", "Aston Martin", "Lada", "Buick", "Chatenet", "UAZ", "Renault", "Volvo", "Hyundai", "Ford", "Opel", "Mazda", "Volkswagen", "Audi", "Nissan", "Skoda", "Toyota", "Kia", "Suzuki", "Jaguar", "Citroen", "Infiniti", "Honda", "Seat", "Dacia", "Jeep", "Chevrolet", "MG", "Fiat", "MINI", "Maserati", "Porsche", "Peugeot", "Cupra", "Lexus", "Dodge", "BAIC", "Mitsubishi", "Tesla", "RAM", "Chrysler", "Daewoo", "Omoda", "Subaru", "BYD", "Daihatsu", "Leapmotor", "Lancia", "Smart", "Maxus", "Jaecoo", "Abarth", "Pontiac", "SARINI", "Microcar", "Cadillac", "Lamborghini", "GMC", "Bentley", "Saab", "Rolls-Royce", "MAN", "Chery", "Aixam", "Ferrari", "Polonez", "Genesis", "Vanderhall", "Iveco", "Mercury", "Acura", "Lincoln", "Alpine", "Hummer", "Oldsmobile", "Warszawa", "DFSK", "Ligier", "Geely", "Trabant", "Aito", "BAW", "Rover", "McLaren", "JAC", "Lotus", "Corvette", "Hongqi", "XPENG", "Isuzu", "Forthing", "Cenntro", "Microlino", "Wartburg", "GWM", "Bestune", "Zhidou", "DKW", "Wołga", "Dongfeng", "Morgan", "Brilliance", "Xiaomi", "GAC", "Voyah", "Santana", "Ineos", "LTI", "Denza", "Tata", "Li", "Nysa", "Wiesmann", "Plymouth", "Gaz", "Polestar", "FOTON", "Seres", "Austin", "e.GO", "Skywell", "Syrena", "Triumph", "Saturn", "DeLorean", "Piaggio", "Asia", "Jetour", "Fisker", "Tarpan", "Jinpeng", "Skyworth", "AVATR", "FAW", "Zastava", "ZEEKR", "Biro", "Żuk", "Vauxhall", "SWM", "NSU", "ORA", "Barkas", "Casalini", "Borgward", "Changan", "WEY", "Lixiang", "Bugatti", "LEVC", "Ariel", "Bentu", "KTM", "Cobra", "DeTomaso", "Lucid", "Riley", "XEV", "NIO", "Delahaye", "Caterham", "Silence", "Donkervoort", "DR MOTOR", "Sportequipe", "Aiways", "ICH-X", "Artega", "TECHART", "Elaris", "Charge", "Westfield", "TVR", "Datsun"
];

export default function App() {
    const [formData, setFormData] = useState<ValuationRequest>({
        marka: CAR_BRANDS[0],
        rok_produkcji: new Date().getFullYear() - 5,
        przebieg: 100000,
        moc_silnika: 150,
        rodzaj_paliwa: 'Benzyna',
        typ_skrzyni_biegow: 'Manualna',
    });

    const [isSubmitting, setIsSubmitting] = useState(false);
    const [result, setResult] = useState<ValuationResponse | null>(null);
    const [error, setError] = useState<string | null>(null);

    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault();
        setIsSubmitting(true);
        setError(null);
        setResult(null);

        const apiUrl = import.meta.env.VITE_API_URL;
        console.log("API URL:", apiUrl);

        if (!apiUrl) {
            setIsSubmitting(false);
            setError("Brak adresu API. Skonfiguruj zmienną środowiskową VITE_API_URL z adresem serwera FastAPI.");
            return;
        }

        try {
            const response = await fetch(apiUrl, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(formData),
            });

            if (!response.ok) {
                throw new Error(`Błąd serwera API (Status: ${response.status})`);
            }

            const data = await response.json();
            setResult(data);
        } catch (err: any) {
            setError(err.message || "Błąd podczas łączenia z FastAPI.");
        } finally {
            setIsSubmitting(false);
        }
    };

    const handleStringChange = (e: React.ChangeEvent<HTMLInputElement | HTMLSelectElement>) => {
        const {name, value} = e.target;
        setFormData((prev) => ({...prev, [name]: value}));
    };

    const handleNumberChange = (e: React.ChangeEvent<HTMLInputElement>) => {
        const {name, value} = e.target;
        setFormData((prev) => ({...prev, [name]: Number(value)}));
    };

    return (
        <div
            className="min-h-screen bg-slate-50 text-slate-900 flex flex-col font-sans overflow-auto lg:overflow-hidden">
            {/* Header Section */}
            <header
                className="h-20 border-b border-slate-200 bg-white px-6 lg:px-12 flex items-center justify-between shrink-0">
                <div className="flex items-center gap-3">
                    <span className="text-2xl font-black tracking-tighter text-slate-900 uppercase">Valauto</span>
                </div>
            </header>

            {/* Main Workspace */}
            <main className="flex-1 flex flex-col lg:flex-row px-6 lg:px-12 py-10 gap-10 lg:overflow-hidden">

                {/* Input Column (Form) */}
                <section
                    className="w-full lg:w-[440px] flex flex-col bg-white rounded-3xl border border-slate-200 shadow-sm overflow-hidden shrink-0 lg:h-full">
                    <div className="p-8 border-b border-slate-100 bg-slate-50/50 shrink-0">
                        <h2 className="text-xs font-black uppercase tracking-[0.2em] text-slate-400">Konfigurator
                            Wyceny</h2>
                        <p className="text-lg font-bold text-slate-800 mt-1">Wprowadź dane pojazdu</p>
                    </div>

                    <div className="p-8 flex-1 overflow-y-auto">
                        <form onSubmit={handleSubmit} className="flex flex-col gap-5 h-full">
                            <div className="space-y-1">
                                <label className="text-[10px] font-bold text-slate-500 uppercase tracking-wider">Marka i
                                    Model</label>
                                <div className="relative">
                                    <CustomSelect
                                        name="marka"
                                        value={formData.marka}
                                        options={CAR_BRANDS}
                                        onChange={handleStringChange}
                                    />
                                </div>
                            </div>

                            <div className="grid grid-cols-2 gap-4">
                                <div className="space-y-1">
                                    <label className="text-[10px] font-bold text-slate-500 uppercase tracking-wider">Rok
                                        produkcji</label>
                                    <input
                                        type="number"
                                        name="rok_produkcji"
                                        required
                                        min="1900"
                                        max={new Date().getFullYear() + 1}
                                        value={formData.rok_produkcji}
                                        onChange={handleNumberChange}
                                        placeholder="2019"
                                        className="w-full px-4 py-3 bg-slate-50 border border-slate-200 rounded-xl focus:ring-2 focus:ring-slate-900/10 focus:border-slate-900 outline-none text-sm transition-all"
                                    />
                                </div>
                                <div className="space-y-1">
                                    <label className="text-[10px] font-bold text-slate-500 uppercase tracking-wider">Przebieg
                                        (km)</label>
                                    <input
                                        type="number"
                                        name="przebieg"
                                        required
                                        min="0"
                                        step="1000"
                                        value={formData.przebieg}
                                        onChange={handleNumberChange}
                                        placeholder="145000"
                                        className="w-full px-4 py-3 bg-slate-50 border border-slate-200 rounded-xl focus:ring-2 focus:ring-slate-900/10 focus:border-slate-900 outline-none text-sm transition-all"
                                    />
                                </div>
                            </div>

                            <div className="space-y-1">
                                <label className="text-[10px] font-bold text-slate-500 uppercase tracking-wider">Moc
                                    silnika (KM)</label>
                                <input
                                    type="number"
                                    name="moc_silnika"
                                    required
                                    min="1"
                                    value={formData.moc_silnika}
                                    onChange={handleNumberChange}
                                    placeholder="150"
                                    className="w-full px-4 py-3 bg-slate-50 border border-slate-200 rounded-xl focus:ring-2 focus:ring-slate-900/10 focus:border-slate-900 outline-none text-sm transition-all"
                                />
                            </div>

                            <div className="grid grid-cols-2 gap-4">
                                <div className="space-y-1">
                                    <label className="text-[10px] font-bold text-slate-500 uppercase tracking-wider">Rodzaj
                                        paliwa</label>
                                    <CustomSelect
                                        name="rodzaj_paliwa"
                                        value={formData.rodzaj_paliwa}
                                        options={['Benzyna', 'Diesel', 'LPG', 'Hybryda', 'Elektryczny']}
                                        onChange={handleStringChange}
                                    />
                                </div>
                                <div className="space-y-1">
                                    <label className="text-[10px] font-bold text-slate-500 uppercase tracking-wider">Skrzynia
                                        biegów</label>
                                    <CustomSelect
                                        name="typ_skrzyni_biegow"
                                        value={formData.typ_skrzyni_biegow}
                                        options={['Manualna', 'Automatyczna']}
                                        onChange={handleStringChange}
                                    />
                                </div>
                            </div>

                            <button
                                type="submit"
                                disabled={isSubmitting}
                                className={`mt-4 lg:mt-auto w-full py-4 rounded-2xl font-bold uppercase tracking-widest text-sm transition-all flex items-center justify-center gap-3 ${
                                    isSubmitting
                                        ? 'bg-slate-700 text-white cursor-not-allowed'
                                        : 'bg-slate-900 text-white hover:shadow-lg'
                                }`}
                            >
                                {isSubmitting ? (
                                    <>
                                        <svg className="animate-spin h-4 w-4 text-white"
                                             xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                                            <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor"
                                                    strokeWidth="4"></circle>
                                            <path className="opacity-75" fill="currentColor"
                                                  d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                                        </svg>
                                        <span>Analizowanie...</span>
                                    </>
                                ) : (
                                    <>
                                        <span>Analizuj Wartość</span>
                                        <Search className="w-4 h-4"/>
                                    </>
                                )}
                            </button>
                        </form>
                    </div>
                </section>

                {/* Output Column (Analysis) */}
                <section className="flex-1 flex flex-col gap-6 lg:overflow-y-auto">

                    <AnimatePresence mode="wait">
                        {error && (
                            <motion.div
                                key="error"
                                initial={{opacity: 0, scale: 0.95}}
                                animate={{opacity: 1, scale: 1}}
                                exit={{opacity: 0, scale: 0.95}}
                                className="bg-red-50 border border-red-200 rounded-3xl p-6 lg:p-10 flex flex-col space-y-2 shadow-sm"
                            >
                                <div className="flex items-center space-x-3">
                                    <AlertCircle className="text-red-500 h-6 w-6"/>
                                    <h3 className="font-bold text-red-900 text-lg">Problem z połączeniem</h3>
                                </div>
                                <p className="text-red-700 text-sm pl-9">{error}</p>
                            </motion.div>
                        )}

                        {!error && !result && !isSubmitting && (
                            <motion.div
                                key="empty"
                                initial={{opacity: 0}}
                                animate={{opacity: 1}}
                                exit={{opacity: 0}}
                                className="flex-1 flex flex-col items-center justify-center text-slate-400 h-[400px] border-2 border-dashed border-slate-200 rounded-[2.5rem]"
                            >
                                <Car className="h-16 w-16 mb-4 opacity-50"/>
                                <p className="font-medium text-sm">Wypełnij formularz, aby zobaczyć wycenę.</p>
                            </motion.div>
                        )}

                        {result && !error && (
                            <motion.div
                                key="result"
                                initial={{opacity: 0, scale: 0.95}}
                                animate={{opacity: 1, scale: 1}}
                                exit={{opacity: 0, scale: 0.95}}
                                className="flex flex-col gap-6 h-full"
                            >
                                {/* Primary Result Display */}
                                <div
                                    className="bg-slate-900 rounded-[2.5rem] p-8 lg:p-10 text-white flex flex-col justify-between relative overflow-hidden">
                                    <div className="relative z-10">
                                        <p className="text-slate-400 text-xs font-bold uppercase tracking-[0.2em] mb-4">Szacowana
                                            Wartość Rynkowa</p>
                                        <div className="flex items-baseline gap-4 flex-wrap">
                      <span className="text-6xl lg:text-[84px] font-black leading-none tracking-tighter">
                        {result.price ? result.price.toLocaleString('pl-PL') : 'Brak'}
                      </span>
                                            <span className="text-2xl font-bold text-slate-500">
                        PLN
                      </span>
                                        </div>
                                    </div>

                                    <div
                                        className="relative z-10 grid grid-cols-2 sm:grid-cols-3 gap-6 lg:gap-10 mt-12 pt-8 border-t border-slate-800">
                                        <div>
                                            <p className="text-[10px] font-bold text-slate-500 uppercase mb-1">Płynność</p>
                                            <p className="text-lg lg:text-xl font-bold text-emerald-400 uppercase">Wysoka</p>
                                        </div>
                                        <div>
                                            <p className="text-[10px] font-bold text-slate-500 uppercase mb-1">Trend</p>
                                            <p className="text-lg lg:text-xl font-bold text-slate-200 uppercase">Stabilny</p>
                                        </div>
                                        <div className="col-span-2 sm:col-span-1">
                                            <p className="text-[10px] font-bold text-slate-500 uppercase mb-1">Zainteresowanie</p>
                                            <p className="text-lg lg:text-xl font-bold text-blue-400 uppercase">Rosnące</p>
                                        </div>
                                    </div>

                                    {/* Abstract Geometric Background */}
                                    <div
                                        className="absolute -right-16 -top-16 w-64 h-64 border-[40px] border-white/5 rounded-full pointer-events-none"></div>
                                    <div
                                        className="absolute left-1/2 -bottom-24 w-48 h-48 bg-emerald-500/10 blur-3xl pointer-events-none"></div>
                                </div>

                                {/* Secondary Data Grid */}
                                <div className="grid grid-cols-1 sm:grid-cols-2 gap-6 pb-6 lg:pb-0">
                                    <div className="bg-white rounded-3xl border border-slate-200 p-8 flex flex-col">
                                        <div
                                            className="w-10 h-10 rounded-full bg-slate-100 flex items-center justify-center text-slate-900 mb-4 shrink-0">
                                            <svg className="w-5 h-5" fill="none" stroke="currentColor"
                                                 viewBox="0 0 24 24">
                                                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2"
                                                      d="M13 7h8m0 0v8m0-8l-8 8-4-4-6 6"></path>
                                            </svg>
                                        </div>
                                        <h3 className="text-sm font-bold text-slate-900 mb-1">Predykcja Ceny</h3>
                                        <p className="text-xs text-slate-400 mb-4">Przewidywana zmiana wartości w ciągu
                                            12 miesięcy</p>
                                        <p className="text-3xl font-black text-slate-900 mt-auto">-3.4%</p>
                                    </div>

                                    <div className="bg-white rounded-3xl border border-slate-200 p-8 flex flex-col">
                                        <div
                                            className="w-10 h-10 rounded-full bg-slate-100 flex items-center justify-center text-slate-900 mb-4 shrink-0">
                                            <svg className="w-5 h-5" fill="none" stroke="currentColor"
                                                 viewBox="0 0 24 24">
                                                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2"
                                                      d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z"></path>
                                            </svg>
                                        </div>
                                        <h3 className="text-sm font-bold text-slate-900 mb-1">Czas Sprzedaży</h3>
                                        <p className="text-xs text-slate-400 mb-4">Średni czas trwania ogłoszenia dla
                                            tego modelu</p>
                                        <p className="text-3xl font-black text-slate-900 mt-auto">24 dni</p>
                                    </div>
                                </div>

                            </motion.div>
                        )}
                    </AnimatePresence>

                </section>
            </main>

            {/* Footer Section */}
            <footer
                className="h-12 px-6 lg:px-12 border-t border-slate-200 bg-white flex items-center justify-between shrink-0">
                <p className="text-[10px] font-bold text-slate-400 uppercase tracking-widest hidden sm:block">© {new Date().getFullYear()} Valauto
                    Intelligent Pricing</p>
            </footer>
        </div>
    );
}
