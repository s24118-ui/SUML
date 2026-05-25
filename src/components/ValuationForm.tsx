import React, {useState} from 'react';
import {Search} from 'lucide-react';
import {ValuationRequest} from '../types';
import {CAR_BRANDS, FUEL_TYPES, TRANSMISSION_TYPES} from '../constants/carBrands';
import {CustomSelect} from './CustomSelect';

interface ValuationFormProps {
    isSubmitting: boolean;
    onSubmit: (data: ValuationRequest) => void;
}

export function ValuationForm({isSubmitting, onSubmit}: ValuationFormProps) {
    const [formData, setFormData] = useState<ValuationRequest>({
        marka: CAR_BRANDS[0],
        rok_produkcji: new Date().getFullYear() - 5,
        przebieg: 100000,
        moc_silnika: 150,
        rodzaj_paliwa: 'Benzyna',
        typ_skrzyni_biegow: 'Manualna',
    });

    const handleSubmit = (e: React.FormEvent) => {
        e.preventDefault();
        onSubmit(formData);
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
        <section
            className="flex flex-col bg-white rounded-3xl border border-slate-200 shadow-sm overflow-hidden shrink-0 lg:h-full">
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
                            <label className="text-[10px] font-bold text-slate-500 uppercase tracking-wider">Rodzaj
                                paliwa</label>
                            <CustomSelect
                                name="rodzaj_paliwa"
                                value={formData.rodzaj_paliwa}
                                options={FUEL_TYPES}
                                onChange={handleStringChange}
                            />
                        </div>
                        <div className="space-y-1">
                            <label className="text-[10px] font-bold text-slate-500 uppercase tracking-wider">Skrzynia
                                biegów</label>
                            <CustomSelect
                                name="typ_skrzyni_biegow"
                                value={formData.typ_skrzyni_biegow}
                                options={TRANSMISSION_TYPES}
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
    );
}
