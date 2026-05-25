import {motion} from 'motion/react';
import {Car} from 'lucide-react';

export function EmptyState() {
    return (
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
    );
}
