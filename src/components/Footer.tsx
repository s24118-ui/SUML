export function Footer() {
    return (
        <footer
            className="h-12 px-6 lg:px-12 border-t border-slate-200 bg-white flex items-center justify-between shrink-0">
            <p className="text-[10px] font-bold text-slate-400 uppercase tracking-widest hidden sm:block">© {new Date().getFullYear()} Valauto
                Intelligent Pricing</p>
        </footer>
    );
}
