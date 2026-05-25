import {useState, useRef, useEffect} from 'react';
import {motion, AnimatePresence} from 'motion/react';
import {ChevronDown} from 'lucide-react';

interface CustomSelectChangeEvent {
    target: {
        name: string;
        value: string;
    };
}

interface SelectProps {
    name: string;
    value: string;
    options: readonly string[];
    onChange: (e: CustomSelectChangeEvent) => void;
}

export function CustomSelect({name, value, options, onChange}: SelectProps) {
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
