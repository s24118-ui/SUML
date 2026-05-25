import {motion} from 'motion/react';
import {ValuationResponse} from '../types';

interface ResultDisplayProps {
    result: ValuationResponse;
}

export function ResultDisplay({result}: ResultDisplayProps) {
    return (
        <motion.div
            key="result"
            initial={{opacity: 0, scale: 0.95}}
            animate={{opacity: 1, scale: 1}}
            exit={{opacity: 0, scale: 0.95}}
            className="flex flex-col gap-6 h-full"
        >
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
                    className="absolute -right-16 -top-16 w-64 h-64 border-[40px] border-white/5 rounded-full pointer-events-none"></div>
                <div
                    className="absolute left-1/2 -bottom-24 w-48 h-48 bg-emerald-500/10 blur-3xl pointer-events-none"></div>
            </div>
        </motion.div>
    );
}
