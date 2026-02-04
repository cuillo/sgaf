import React, { useState, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { Printer, RefreshCw, AlertTriangle, CheckCircle, Search, Filter, Droplet, MapPin, Hash, Activity } from 'lucide-react';
import api from '../../api';

const PrinterCard = ({ printer, onRefresh }) => {
    const [refreshing, setRefreshing] = useState(false);

    const handleRefresh = async () => {
        setRefreshing(true);
        try {
            await onRefresh(printer.id);
        } finally {
            setRefreshing(false);
        }
    };

    const getStatusColor = () => {
        if (!printer.last_ok && printer.last_check) return 'bg-red-100 text-red-600 border-red-200';
        if (printer.last_errors && printer.last_errors.length > 0) return 'bg-yellow-100 text-yellow-600 border-yellow-200';
        if (printer.last_ok) return 'bg-emerald-100 text-emerald-600 border-emerald-200';
        return 'bg-slate-100 text-slate-500 border-slate-200';
    };

    const StatusIcon = () => {
        if (!printer.last_ok && printer.last_check) return <AlertTriangle className="w-5 h-5" />;
        if (printer.last_errors && printer.last_errors.length > 0) return <AlertTriangle className="w-5 h-5" />;
        if (printer.last_ok) return <CheckCircle className="w-5 h-5" />;
        return <Activity className="w-5 h-5" />;
    };

    const TonerBar = ({ color, level, label }) => {
        if (level === null || level === undefined) return null;

        // Map color names to tailwind classes
        const colorMap = {
            black: 'bg-slate-900',
            cyan: 'bg-cyan-500',
            magenta: 'bg-pink-500',
            yellow: 'bg-yellow-400',
        };

        return (
            <div className="flex flex-col gap-1 w-full">
                <div className="flex justify-between text-xs font-medium text-slate-600">
                    <span className="capitalize">{label}</span>
                    <span>{level}%</span>
                </div>
                <div className="w-full bg-slate-200 rounded-full h-2 overflow-hidden">
                    <motion.div
                        initial={{ width: 0 }}
                        animate={{ width: `${level}%` }}
                        transition={{ duration: 0.5, ease: "easeOut" }}
                        className={`h-full rounded-full ${colorMap[color] || 'bg-slate-500'}`}
                    />
                </div>
            </div>
        );
    };

    return (
        <motion.div
            layout
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0, scale: 0.95 }}
            className="bg-white rounded-2xl shadow-sm border border-slate-200 overflow-hidden hover:shadow-lg transition-all duration-300 group"
        >
            <div className="p-5">
                <div className="flex justify-between items-start mb-4">
                    <div className="flex items-center gap-3">
                        <div className={`w-10 h-10 rounded-xl flex items-center justify-center ${getStatusColor()} bg-opacity-20`}>
                            <Printer className="w-5 h-5" />
                        </div>
                        <div>
                            <h3 className="font-bold text-slate-800 line-clamp-1 group-hover:text-blue-600 transition-colors">{printer.name}</h3>
                            <div className="flex items-center gap-1 text-xs text-slate-500">
                                <MapPin className="w-3 h-3" />
                                {printer.location} {printer.floor && `• ${printer.floor}`}
                            </div>
                        </div>
                    </div>
                    <div className={`px-2 py-1 rounded-full text-xs font-medium flex items-center gap-1 border ${getStatusColor()}`}>
                        <StatusIcon />
                        <span className="hidden sm:inline">
                            {printer.last_ok ? 'Online' : (printer.last_check ? 'Offline' : 'Unknown')}
                        </span>
                    </div>
                </div>

                <div className="grid grid-cols-2 gap-2 mb-4 text-xs text-slate-500 bg-slate-50 p-3 rounded-xl border border-slate-100">
                    <div className="flex items-center gap-2">
                        <Hash className="w-3 h-3 text-slate-400" />
                        <span className="font-mono">{printer.ip_address}</span>
                    </div>
                    {printer.serial_number && (
                        <div className="flex items-center gap-2" title="Serial Number">
                            <span className="font-mono truncate">{printer.serial_number}</span>
                        </div>
                    )}
                </div>

                {/* Toner Levels */}
                <div className="space-y-2 mb-4">
                    {printer.toner.black !== null ? (
                        <TonerBar color="black" level={printer.toner.black} label="Black" />
                    ) : (
                        <div className="text-xs text-slate-400 text-center py-2 flex items-center justify-center gap-2">
                            <Droplet className="w-3 h-3" /> No toner data
                        </div>
                    )}
                    {printer.type === 'COLOR' && (
                        <>
                            <TonerBar color="cyan" level={printer.toner.cyan} label="Cyan" />
                            <TonerBar color="magenta" level={printer.toner.magenta} label="Magenta" />
                            <TonerBar color="yellow" level={printer.toner.yellow} label="Yellow" />
                        </>
                    )}
                </div>

                {printer.last_errors && printer.last_errors.length > 0 && (
                    <div className="mb-4 bg-red-50 border border-red-100 p-3 rounded-xl text-xs text-red-600 flex items-start gap-2">
                        <AlertTriangle className="w-4 h-4 flex-shrink-0 mt-0.5" />
                        <ul className="list-disc list-inside">
                            {printer.last_errors.map((err, idx) => (
                                <li key={idx}>{err}</li>
                            ))}
                        </ul>
                    </div>
                )}
            </div>

            <div className="bg-slate-50 px-5 py-3 border-t border-slate-100 flex justify-between items-center text-xs text-slate-500">
                <span>Updated: {printer.last_check || 'Never'}</span>
                <button
                    onClick={handleRefresh}
                    disabled={refreshing}
                    className={`p-2 rounded-lg hover:bg-white hover:shadow-sm transition-all text-slate-600 ${refreshing ? 'animate-spin text-blue-600' : ''}`}
                    title="Refresh Status"
                >
                    <RefreshCw className="w-4 h-4" />
                </button>
            </div>
        </motion.div>
    );
};

const ImpresorasDashboard = () => {
    const [printers, setPrinters] = useState([]);
    const [loading, setLoading] = useState(true);
    const [refreshingAll, setRefreshingAll] = useState(false);
    const [filter, setFilter] = useState('all'); // all, error, low-toner, offline

    useEffect(() => {
        fetchPrinters();
    }, []);

    const fetchPrinters = async () => {
        try {
            const response = await api.get('printers/');
            setPrinters(response.data);
        } catch (error) {
            console.error("Error fetching printers:", error);
        } finally {
            setLoading(false);
        }
    };

    const handleRefreshPrinter = async (id) => {
        try {
            const response = await api.post(`printers/${id}/refresh/`);
            if (response.data.success) {
                setPrinters(prev => prev.map(p => p.id === id ? response.data.printer : p));
            }
        } catch (error) {
            console.error("Error refreshing printer:", error);
        }
    };

    const handleRefreshAll = async () => {
        setRefreshingAll(true);
        try {
            // Note: In a real scenario with many printers, this might timeout or take long.
            // Ideally we'd trigger a background job or handle it one by one.
            // For now given the legacy code did it synchronously-ish (asyncio loop but one http request wait), we'll do:
            await api.post('printers/refresh_all/');
            await fetchPrinters();
        } catch (error) {
            console.error("Error refreshing all:", error);
        } finally {
            setRefreshingAll(false);
        }
    };

    const filteredPrinters = printers.filter(p => {
        if (filter === 'all') return true;
        if (filter === 'error') return (p.last_errors && p.last_errors.length > 0) || (!p.last_ok && p.last_check);
        if (filter === 'offline') return !p.last_ok && p.last_check;
        // Simple low toner check < 10%
        if (filter === 'low-toner') {
            const low = (val) => val !== null && val < 20;
            return low(p.toner.black) || low(p.toner.cyan) || low(p.toner.magenta) || low(p.toner.yellow);
        }
        return true;
    });

    return (
        <div className="space-y-6">
            <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
                <div>
                    <h1 className="text-2xl font-bold text-slate-800">Monitoreo de Impresoras</h1>
                    <p className="text-slate-500">Gestión y estado de {printers.length} dispositivos en tiempo real</p>
                </div>
                <div className="flex items-center gap-2">
                    <button
                        onClick={handleRefreshAll}
                        disabled={refreshingAll}
                        className="flex items-center gap-2 bg-blue-600 text-white px-4 py-2 rounded-xl hover:bg-blue-700 transition-colors shadow-lg shadow-blue-600/20 disabled:opacity-70 disabled:cursor-not-allowed"
                    >
                        <RefreshCw className={`w-4 h-4 ${refreshingAll ? 'animate-spin' : ''}`} />
                        <span>{refreshingAll ? 'Actualizando...' : 'Actualizar Todo'}</span>
                    </button>
                    {/* Add Printer button could go here */}
                </div>
            </div>

            {/* Filters */}
            <div className="flex items-center gap-2 overflow-x-auto pb-2">
                {[
                    { id: 'all', label: 'Todos', count: printers.length },
                    { id: 'error', label: 'Con Errores', count: printers.filter(p => (p.last_errors && p.last_errors.length > 0) || (!p.last_ok && p.last_check)).length, color: 'text-red-500' },
                    {
                        id: 'low-toner', label: 'Toner Bajo (<20%)', count: printers.filter(p => {
                            const low = (val) => val !== null && val < 20;
                            return low(p.toner.black) || low(p.toner.cyan) || low(p.toner.magenta) || low(p.toner.yellow);
                        }).length, color: 'text-yellow-500'
                    }
                ].map(f => (
                    <button
                        key={f.id}
                        onClick={() => setFilter(f.id)}
                        className={`px-4 py-2 rounded-xl text-xs font-medium border transition-all flex items-center gap-2 whitespace-nowrap
                            ${filter === f.id ? 'bg-slate-800 text-white border-slate-800' : 'bg-white text-slate-600 border-slate-200 hover:border-slate-300'}`}
                    >
                        {f.label}
                        <span className={`px-1.5 py-0.5 rounded-full text-[10px] ${filter === f.id ? 'bg-slate-600 text-white' : 'bg-slate-100 text-slate-600'}`}>
                            {f.count}
                        </span>
                    </button>
                ))}
            </div>

            {loading ? (
                <div className="flex items-center justify-center p-20">
                    <RefreshCw className="w-8 h-8 text-blue-600 animate-spin" />
                </div>
            ) : (
                <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6">
                    <AnimatePresence>
                        {filteredPrinters.map(printer => (
                            <PrinterCard
                                key={printer.id}
                                printer={printer}
                                onRefresh={handleRefreshPrinter}
                            />
                        ))}
                    </AnimatePresence>
                    {filteredPrinters.length === 0 && (
                        <div className="col-span-full py-20 text-center text-slate-400 bg-white rounded-3xl border border-dashed border-slate-200">
                            <Printer className="w-12 h-12 mx-auto mb-4 opacity-20" />
                            <p>No se encontraron impresoras con este filtro</p>
                        </div>
                    )}
                </div>
            )}
        </div>
    );
};

export default ImpresorasDashboard;
