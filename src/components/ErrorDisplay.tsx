import {motion} from 'motion/react';
import {AlertCircle} from 'lucide-react';

interface ErrorDisplayProps {
    message: string;
}

export function ErrorDisplay({message}: ErrorDisplayProps) {
    return (
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
            <p className="text-red-700 text-sm pl-9">{message}</p>
        </motion.div>
    );
}
