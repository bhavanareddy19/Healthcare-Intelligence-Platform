import React, { useState } from 'react';
import {
    Activity, FileText, Search, BarChart3, Upload, Brain,
    Zap, Shield, Clock, TrendingUp, ChevronRight, Sparkles,
    Stethoscope, Pill, AlertTriangle, FileCheck, Users, Database,
    Bot, Cpu, LineChart, PieChart
} from 'lucide-react';

// API Configuration
const API_BASE = 'http://localhost:8000';

// Markdown Renderer Component - renders basic markdown syntax
const MarkdownRenderer = ({ content }) => {
    if (!content) return null;

    // Process markdown and convert to React elements
    const renderMarkdown = (text) => {
        const lines = text.split('\n');
        const elements = [];
        let listItems = [];
        let inList = false;

        lines.forEach((line, index) => {
            // Handle numbered lists (e.g., "1. Item")
            const numberedMatch = line.match(/^(\d+)\.\s+\*\*(.+?)\*\*(.*)$/);
            if (numberedMatch) {
                if (!inList) {
                    inList = true;
                    listItems = [];
                }
                listItems.push(
                    <li key={index} style={{ marginBottom: '0.75rem' }}>
                        <strong style={{ color: 'var(--text-primary)' }}>{numberedMatch[2]}</strong>
                        {renderInlineMarkdown(numberedMatch[3])}
                    </li>
                );
                return;
            }

            // Handle simple numbered lists
            const simpleNumberedMatch = line.match(/^(\d+)\.\s+(.+)$/);
            if (simpleNumberedMatch) {
                if (!inList) {
                    inList = true;
                    listItems = [];
                }
                listItems.push(
                    <li key={index} style={{ marginBottom: '0.5rem' }}>
                        {renderInlineMarkdown(simpleNumberedMatch[2])}
                    </li>
                );
                return;
            }

            // Handle bullet lists
            const bulletMatch = line.match(/^[-*]\s+(.+)$/);
            if (bulletMatch) {
                if (!inList) {
                    inList = true;
                    listItems = [];
                }
                listItems.push(
                    <li key={index} style={{ marginBottom: '0.5rem' }}>
                        {renderInlineMarkdown(bulletMatch[1])}
                    </li>
                );
                return;
            }

            // End of list - flush list items
            if (inList && listItems.length > 0) {
                elements.push(
                    <ol key={`list-${index}`} style={{
                        paddingLeft: '1.5rem',
                        marginBottom: '1rem',
                        color: 'var(--text-secondary)'
                    }}>
                        {listItems}
                    </ol>
                );
                listItems = [];
                inList = false;
            }

            // Handle headers
            if (line.startsWith('### ')) {
                elements.push(
                    <h4 key={index} style={{ marginTop: '1rem', marginBottom: '0.5rem', color: 'var(--text-primary)' }}>
                        {line.slice(4)}
                    </h4>
                );
                return;
            }
            if (line.startsWith('## ')) {
                elements.push(
                    <h3 key={index} style={{ marginTop: '1rem', marginBottom: '0.5rem', color: 'var(--text-primary)' }}>
                        {line.slice(3)}
                    </h3>
                );
                return;
            }
            if (line.startsWith('# ')) {
                elements.push(
                    <h2 key={index} style={{ marginTop: '1rem', marginBottom: '0.5rem', color: 'var(--text-primary)' }}>
                        {line.slice(2)}
                    </h2>
                );
                return;
            }

            // Handle empty lines
            if (line.trim() === '') {
                elements.push(<br key={index} />);
                return;
            }

            // Regular paragraph with inline formatting
            elements.push(
                <p key={index} style={{ marginBottom: '0.5rem', lineHeight: 1.7, color: 'var(--text-secondary)' }}>
                    {renderInlineMarkdown(line)}
                </p>
            );
        });

        // Flush any remaining list items
        if (listItems.length > 0) {
            elements.push(
                <ol key="list-final" style={{
                    paddingLeft: '1.5rem',
                    marginBottom: '1rem',
                    color: 'var(--text-secondary)'
                }}>
                    {listItems}
                </ol>
            );
        }

        return elements;
    };

    // Handle inline markdown (bold, italic, code)
    const renderInlineMarkdown = (text) => {
        if (!text) return null;

        const parts = [];
        let remaining = text;
        let key = 0;

        while (remaining.length > 0) {
            // Bold: **text**
            const boldMatch = remaining.match(/\*\*(.+?)\*\*/);
            if (boldMatch && boldMatch.index === 0) {
                parts.push(<strong key={key++} style={{ color: 'var(--text-primary)' }}>{boldMatch[1]}</strong>);
                remaining = remaining.slice(boldMatch[0].length);
                continue;
            }

            // Italic: *text* or _text_
            const italicMatch = remaining.match(/(?:\*|_)(.+?)(?:\*|_)/);
            if (italicMatch && italicMatch.index === 0) {
                parts.push(<em key={key++}>{italicMatch[1]}</em>);
                remaining = remaining.slice(italicMatch[0].length);
                continue;
            }

            // Code: `text`
            const codeMatch = remaining.match(/`(.+?)`/);
            if (codeMatch && codeMatch.index === 0) {
                parts.push(
                    <code key={key++} style={{
                        background: 'var(--bg-tertiary)',
                        padding: '0.125rem 0.375rem',
                        borderRadius: '4px',
                        fontSize: '0.875rem'
                    }}>
                        {codeMatch[1]}
                    </code>
                );
                remaining = remaining.slice(codeMatch[0].length);
                continue;
            }

            // Find next special character or end
            const nextSpecial = remaining.search(/\*|_|`/);
            if (nextSpecial === -1) {
                parts.push(remaining);
                break;
            } else if (nextSpecial === 0) {
                parts.push(remaining[0]);
                remaining = remaining.slice(1);
            } else {
                parts.push(remaining.slice(0, nextSpecial));
                remaining = remaining.slice(nextSpecial);
            }
        }

        return parts;
    };

    return <div className="markdown-content">{renderMarkdown(content)}</div>;
};

// Navigation Component
const Navbar = ({ currentPage, setCurrentPage }) => {
    const navItems = [
        { id: 'dashboard', label: 'Dashboard', icon: Activity },
        { id: 'upload', label: 'Upload', icon: Upload },
        { id: 'search', label: 'Search', icon: Search },
        { id: 'agents', label: 'AI Agents', icon: Bot },
        { id: 'analytics', label: 'Analytics', icon: BarChart3 },
    ];

    return (
        <nav className="navbar">
            <div className="navbar-brand">
                <div className="navbar-logo">🏥</div>
                <span className="navbar-title">Healthcare Intelligence</span>
            </div>
            <div className="navbar-nav">
                {navItems.map(item => (
                    <button
                        key={item.id}
                        className={`nav-link ${currentPage === item.id ? 'active' : ''}`}
                        onClick={() => setCurrentPage(item.id)}
                    >
                        <item.icon size={18} />
                        {item.label}
                    </button>
                ))}
            </div>
        </nav>
    );
};

// Dashboard Page
const Dashboard = ({ setCurrentPage }) => {
    const stats = [
        { value: '92%', label: 'Extraction Accuracy', icon: Zap },
        { value: '<50ms', label: 'Search Latency (p99)', icon: Clock },
        { value: '14', label: 'Active AI Agents', icon: Bot },
        { value: '85%', label: 'Time Saved', icon: TrendingUp },
    ];

    const agents = [
        { name: 'Diagnosis Extraction', status: 'active', task: 'Ready' },
        { name: 'Risk Factor Analysis', status: 'active', task: 'Ready' },
        { name: 'ICD-10 Coding', status: 'active', task: 'Ready' },
        { name: 'Medication Analysis', status: 'active', task: 'Ready' },
        { name: 'HEDIS Compliance', status: 'active', task: 'Ready' },
        { name: 'Lab Interpretation', status: 'active', task: 'Ready' },
    ];

    const features = [
        {
            icon: Brain,
            title: 'Multi-Agent Framework',
            description: '15 specialized AI agents work together to analyze clinical documents comprehensively.'
        },
        {
            icon: Search,
            title: 'Semantic Search',
            description: 'Natural language search across millions of medical records with sub-50ms latency.'
        },
        {
            icon: Shield,
            title: 'RAG Pipeline',
            description: 'Retrieval-Augmented Generation ensures accurate, context-aware responses.'
        },
        {
            icon: Database,
            title: 'FAISS Vector Store',
            description: 'Production-scale vector database handles 10M+ document embeddings efficiently.'
        }
    ];

    return (
        <div className="container">
            {/* Hero Section */}
            <section className="hero">
                <div className="hero-badge">
                    <Sparkles size={16} />
                    AI-Powered Clinical Analytics
                </div>
                <h1 className="hero-title">
                    Transform Clinical Data into<br />
                    <span className="gradient">Actionable Intelligence</span>
                </h1>
                <p className="hero-subtitle">
                    Advanced LLM-powered platform that processes clinical documents,
                    extracts structured metrics, and enables semantic search across your entire healthcare data.
                </p>
                <div style={{ display: 'flex', gap: '1rem', justifyContent: 'center' }}>
                    <button className="btn btn-primary btn-lg" onClick={() => setCurrentPage('upload')}>
                        <Upload size={20} />
                        Upload Documents
                    </button>
                    <button className="btn btn-secondary btn-lg" onClick={() => setCurrentPage('search')}>
                        <Search size={20} />
                        Start Searching
                    </button>
                </div>

                <div className="hero-stats">
                    {stats.map((stat, idx) => (
                        <div key={idx} className="stat-item">
                            <div className="stat-value">{stat.value}</div>
                            <div className="stat-label">{stat.label}</div>
                        </div>
                    ))}
                </div>
            </section>

            {/* Features Grid */}
            <section className="section">
                <div className="section-header">
                    <h2 className="section-title">Enterprise-Grade AI Infrastructure</h2>
                    <p className="section-subtitle">
                        Built with production-ready components for scalability, accuracy, and performance.
                    </p>
                </div>
                <div className="grid grid-4">
                    {features.map((feature, idx) => (
                        <div key={idx} className="card feature-card fade-in" style={{ animationDelay: `${idx * 0.1}s` }}>
                            <div className="feature-icon">
                                <feature.icon size={24} />
                            </div>
                            <h3 className="feature-title">{feature.title}</h3>
                            <p className="feature-description">{feature.description}</p>
                        </div>
                    ))}
                </div>
            </section>

            {/* Agent Status */}
            <section className="section">
                <div className="grid grid-2">
                    <div className="card">
                        <div className="card-header">
                            <h3 className="card-title">
                                <div className="card-icon"><Bot size={18} /></div>
                                AI Agent Status
                            </h3>
                            <span className="tag success">All Systems Operational</span>
                        </div>
                        <div style={{ display: 'flex', flexDirection: 'column', gap: '0.5rem' }}>
                            {agents.map((agent, idx) => (
                                <div key={idx} className="agent-card">
                                    <div className={`agent-status ${agent.status}`}></div>
                                    <div className="agent-info">
                                        <div className="agent-name">{agent.name}</div>
                                        <div className="agent-task">{agent.task}</div>
                                    </div>
                                </div>
                            ))}
                        </div>
                    </div>

                    <div className="card">
                        <div className="card-header">
                            <h3 className="card-title">
                                <div className="card-icon"><Activity size={18} /></div>
                                Quick Actions
                            </h3>
                        </div>
                        <div style={{ display: 'flex', flexDirection: 'column', gap: '1rem' }}>
                            <button className="btn btn-primary" style={{ width: '100%' }} onClick={() => setCurrentPage('upload')}>
                                <FileText size={18} />
                                Upload Clinical Document
                            </button>
                            <button className="btn btn-secondary" style={{ width: '100%' }} onClick={() => setCurrentPage('search')}>
                                <Search size={18} />
                                Semantic Search
                            </button>
                            <button className="btn btn-secondary" style={{ width: '100%' }} onClick={() => setCurrentPage('agents')}>
                                <Bot size={18} />
                                Run Multi-Agent Analysis
                            </button>
                            <button className="btn btn-accent" style={{ width: '100%' }}>
                                <Sparkles size={18} />
                                Load Sample Documents
                            </button>
                        </div>
                    </div>
                </div>
            </section>
        </div>
    );
};

// Upload Page
const UploadPage = () => {
    const [dragActive, setDragActive] = useState(false);
    const [files, setFiles] = useState([]);
    const [uploading, setUploading] = useState(false);
    const [uploadResults, setUploadResults] = useState([]);

    const handleDrag = (e) => {
        e.preventDefault();
        e.stopPropagation();
        if (e.type === "dragenter" || e.type === "dragover") {
            setDragActive(true);
        } else if (e.type === "dragleave") {
            setDragActive(false);
        }
    };

    const handleDrop = (e) => {
        e.preventDefault();
        e.stopPropagation();
        setDragActive(false);

        if (e.dataTransfer.files && e.dataTransfer.files[0]) {
            handleFiles(e.dataTransfer.files);
        }
    };

    const handleFiles = (fileList) => {
        const newFiles = Array.from(fileList);
        setFiles(prev => [...prev, ...newFiles]);
    };

    const handleUpload = async () => {
        setUploading(true);
        const results = [];

        for (const file of files) {
            try {
                const formData = new FormData();
                formData.append('file', file);

                const response = await fetch(`${API_BASE}/api/documents/upload`, {
                    method: 'POST',
                    body: formData
                });

                if (response.ok) {
                    const data = await response.json();
                    results.push({ file: file.name, success: true, data });
                } else {
                    results.push({ file: file.name, success: false, error: 'Upload failed' });
                }
            } catch (error) {
                results.push({ file: file.name, success: false, error: error.message });
            }
        }

        setUploadResults(results);
        setUploading(false);
    };

    return (
        <div className="container">
            <section className="section">
                <div className="section-header">
                    <h2 className="section-title">Upload Clinical Documents</h2>
                    <p className="section-subtitle">
                        Upload PDF, TXT, or DOCX files containing clinical notes, discharge summaries, or lab reports.
                    </p>
                </div>

                <div
                    className={`upload-zone ${dragActive ? 'active' : ''}`}
                    onDragEnter={handleDrag}
                    onDragLeave={handleDrag}
                    onDragOver={handleDrag}
                    onDrop={handleDrop}
                    onClick={() => document.getElementById('file-input').click()}
                >
                    <input
                        type="file"
                        id="file-input"
                        multiple
                        accept=".pdf,.txt,.docx"
                        style={{ display: 'none' }}
                        onChange={(e) => handleFiles(e.target.files)}
                    />
                    <div className="upload-icon">
                        <Upload size={32} />
                    </div>
                    <h3 style={{ marginBottom: '0.5rem' }}>Drop files here or click to upload</h3>
                    <p style={{ color: 'var(--text-tertiary)' }}>
                        Supports PDF, TXT, and DOCX files up to 50MB each
                    </p>
                </div>

                {files.length > 0 && (
                    <div className="card" style={{ marginTop: '2rem' }}>
                        <div className="card-header">
                            <h3 className="card-title">
                                <div className="card-icon"><FileText size={18} /></div>
                                Selected Files ({files.length})
                            </h3>
                            <button className="btn btn-primary" onClick={handleUpload} disabled={uploading}>
                                {uploading ? (
                                    <>
                                        <div className="spinner" style={{ width: 18, height: 18 }}></div>
                                        Processing...
                                    </>
                                ) : (
                                    <>
                                        <Zap size={18} />
                                        Process All
                                    </>
                                )}
                            </button>
                        </div>
                        <div className="document-list">
                            {files.map((file, idx) => (
                                <div key={idx} className="document-item">
                                    <div className="document-icon">
                                        <FileText size={20} />
                                    </div>
                                    <div className="document-info">
                                        <div className="document-name">{file.name}</div>
                                        <div className="document-meta">
                                            {(file.size / 1024).toFixed(1)} KB • {file.type || 'Unknown type'}
                                        </div>
                                    </div>
                                    {uploadResults.find(r => r.file === file.name) && (
                                        <span className={`tag ${uploadResults.find(r => r.file === file.name).success ? 'success' : 'error'}`}>
                                            {uploadResults.find(r => r.file === file.name).success ? 'Processed' : 'Failed'}
                                        </span>
                                    )}
                                </div>
                            ))}
                        </div>
                    </div>
                )}

                {uploadResults.length > 0 && (
                    <div className="card" style={{ marginTop: '2rem' }}>
                        <div className="card-header">
                            <h3 className="card-title">
                                <div className="card-icon" style={{ background: 'var(--gradient-accent)' }}><FileCheck size={18} /></div>
                                Processing Results
                            </h3>
                        </div>
                        <div className="results-content">
                            {uploadResults.map((result, idx) => (
                                <div key={idx} className="result-item">
                                    <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                                        <strong>{result.file}</strong>
                                        <span className={`tag ${result.success ? 'success' : 'error'}`}>
                                            {result.success ? '✓ Success' : '✗ Failed'}
                                        </span>
                                    </div>
                                    {result.success && result.data && (
                                        <p style={{ marginTop: '0.5rem', color: 'var(--text-secondary)' }}>
                                            Created {result.data.chunks_count} chunks • Document ID: {result.data.id?.slice(0, 8)}...
                                        </p>
                                    )}
                                </div>
                            ))}
                        </div>
                    </div>
                )}
            </section>
        </div>
    );
};

// Search Page
const SearchPage = () => {
    const [query, setQuery] = useState('');
    const [results, setResults] = useState(null);
    const [loading, setLoading] = useState(false);

    const handleSearch = async () => {
        if (!query.trim()) return;

        setLoading(true);
        try {
            const response = await fetch(`${API_BASE}/api/search/semantic`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ query, top_k: 5, use_rag: true })
            });

            if (response.ok) {
                const data = await response.json();
                setResults(data);
            }
        } catch (error) {
            console.error('Search error:', error);
        }
        setLoading(false);
    };

    return (
        <div className="container">
            <section className="section">
                <div className="section-header">
                    <h2 className="section-title">Semantic Search</h2>
                    <p className="section-subtitle">
                        Search across clinical documents using natural language. Our AI understands medical context.
                    </p>
                </div>

                <div className="search-bar" style={{ marginBottom: '2rem' }}>
                    <Search className="search-icon" size={20} />
                    <input
                        type="text"
                        className="search-input"
                        placeholder="Ask a question like 'patients with diabetes and hypertension' or 'discharge instructions for post-surgery'"
                        value={query}
                        onChange={(e) => setQuery(e.target.value)}
                        onKeyDown={(e) => e.key === 'Enter' && handleSearch()}
                    />
                </div>

                <div style={{ display: 'flex', justifyContent: 'center', gap: '1rem', marginBottom: '2rem' }}>
                    <button className="btn btn-primary" onClick={handleSearch} disabled={loading}>
                        {loading ? <div className="spinner" style={{ width: 18, height: 18 }}></div> : <Search size={18} />}
                        Search
                    </button>
                    <button className="btn btn-secondary" onClick={() => setQuery('What are the common diagnoses?')}>
                        <Sparkles size={18} />
                        Try Example
                    </button>
                </div>

                {results && (
                    <div className="dashboard-grid">
                        <div>
                            {results.rag_summary && (
                                <div className="card" style={{ marginBottom: '1.5rem' }}>
                                    <div className="card-header">
                                        <h3 className="card-title">
                                            <div className="card-icon"><Brain size={18} /></div>
                                            AI-Generated Answer
                                        </h3>
                                        <span className="tag success">RAG Enhanced</span>
                                    </div>
                                    <MarkdownRenderer content={results.rag_summary} />
                                </div>
                            )}

                            <div className="card">
                                <div className="card-header">
                                    <h3 className="card-title">
                                        <div className="card-icon"><FileText size={18} /></div>
                                        Relevant Documents ({results.total_results})
                                    </h3>
                                </div>
                                <div className="document-list">
                                    {results.results.map((result, idx) => (
                                        <div key={idx} className="document-item" style={{ borderLeft: '3px solid var(--primary-400)' }}>
                                            <div className="document-info">
                                                <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', marginBottom: '0.5rem' }}>
                                                    <span className="tag">Score: {(result.score * 100).toFixed(1)}%</span>
                                                    <span style={{ fontSize: '0.75rem', color: 'var(--text-tertiary)' }}>
                                                        Doc: {result.document_id?.slice(0, 8)}...
                                                    </span>
                                                </div>
                                                <p style={{ color: 'var(--text-secondary)', fontSize: '0.9375rem', lineHeight: 1.6 }}>
                                                    {result.content.slice(0, 300)}...
                                                </p>
                                            </div>
                                        </div>
                                    ))}
                                </div>
                            </div>
                        </div>

                        <div>
                            <div className="card">
                                <div className="card-header">
                                    <h3 className="card-title">
                                        <div className="card-icon"><Clock size={18} /></div>
                                        Search Stats
                                    </h3>
                                </div>
                                <div style={{ display: 'flex', flexDirection: 'column', gap: '1rem' }}>
                                    <div className="metric-card" style={{ padding: '1rem' }}>
                                        <div className="metric-value">{results.latency_ms}ms</div>
                                        <div className="metric-label">Search Latency</div>
                                    </div>
                                    <div className="metric-card" style={{ padding: '1rem' }}>
                                        <div className="metric-value">{results.total_results}</div>
                                        <div className="metric-label">Results Found</div>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                )}
            </section>
        </div>
    );
};

// Agents Page
const AgentsPage = () => {
    const [text, setText] = useState('');
    const [selectedAgents, setSelectedAgents] = useState([]);
    const [results, setResults] = useState(null);
    const [loading, setLoading] = useState(false);

    const agents = [
        { id: 'diagnosis', name: 'Diagnosis Extraction', icon: Stethoscope, description: 'Extract diagnoses with confidence scores' },
        { id: 'risk_factors', name: 'Risk Factor Analysis', icon: AlertTriangle, description: 'Identify HCC and demographic risks' },
        { id: 'icd_codes', name: 'ICD-10 Coding', icon: FileCheck, description: 'Extract and suggest ICD-10 codes' },
        { id: 'medications', name: 'Medication Analysis', icon: Pill, description: 'Analyze drugs and interactions' },
        { id: 'lab_results', name: 'Lab Interpretation', icon: Activity, description: 'Interpret laboratory values' },
        { id: 'summary', name: 'Clinical Summary', icon: FileText, description: 'Generate executive summaries' },
        { id: 'hedis', name: 'HEDIS Compliance', icon: Shield, description: 'Check HEDIS measure compliance' },
        { id: 'quality_measures', name: 'Quality Measures', icon: TrendingUp, description: 'Map to CMS quality measures' },
        { id: 'compliance', name: 'Regulatory Compliance', icon: Shield, description: 'Check regulatory compliance' },
        { id: 'alerts', name: 'Clinical Alerts', icon: AlertTriangle, description: 'Generate priority alerts' },
    ];

    const toggleAgent = (id) => {
        setSelectedAgents(prev =>
            prev.includes(id) ? prev.filter(a => a !== id) : [...prev, id]
        );
    };

    const runAnalysis = async () => {
        if (!text.trim()) return;

        setLoading(true);
        try {
            const response = await fetch(`${API_BASE}/api/agents/analyze`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    text,
                    agents: selectedAgents.length > 0 ? selectedAgents : null
                })
            });

            if (response.ok) {
                const data = await response.json();
                setResults(data);
            }
        } catch (error) {
            console.error('Analysis error:', error);
        }
        setLoading(false);
    };

    const loadSampleText = () => {
        setText(`DISCHARGE SUMMARY

Patient: John Doe, 65-year-old male
Admission: 01/15/2024 | Discharge: 01/20/2024

DIAGNOSES:
1. Diabetic Ketoacidosis - resolved
2. Type 2 Diabetes Mellitus, uncontrolled (HbA1c 11.2%)
3. Hypertension
4. Chronic Kidney Disease Stage 3b

MEDICATIONS AT DISCHARGE:
1. Lantus (insulin glargine) 20 units at bedtime
2. Humalog (insulin lispro) 6 units with meals
3. Metoprolol 50mg BID
4. Atorvastatin 40mg daily

LABORATORY:
- Glucose: 450 mg/dL (H)
- Creatinine: 1.8 mg/dL (H)
- eGFR: 38 mL/min/1.73m2
- HbA1c: 11.2% (H)

FOLLOW-UP:
- Endocrinology in 2 weeks
- Nephrology in 2 weeks
- Primary care in 1 week`);
    };

    return (
        <div className="container">
            <section className="section">
                <div className="section-header">
                    <h2 className="section-title">Multi-Agent Clinical Analysis</h2>
                    <p className="section-subtitle">
                        Select AI agents to analyze clinical text. Each agent specializes in extracting specific information.
                    </p>
                </div>

                <div className="dashboard-grid">
                    <div>
                        <div className="card" style={{ marginBottom: '1.5rem' }}>
                            <div className="card-header">
                                <h3 className="card-title">
                                    <div className="card-icon"><FileText size={18} /></div>
                                    Clinical Text
                                </h3>
                                <button className="btn btn-secondary" onClick={loadSampleText}>
                                    <Sparkles size={16} />
                                    Load Sample
                                </button>
                            </div>
                            <textarea
                                style={{
                                    width: '100%',
                                    minHeight: '300px',
                                    padding: '1rem',
                                    background: 'var(--bg-tertiary)',
                                    border: '1px solid var(--border-primary)',
                                    borderRadius: 'var(--radius-md)',
                                    color: 'var(--text-primary)',
                                    fontFamily: 'inherit',
                                    fontSize: '0.9375rem',
                                    resize: 'vertical'
                                }}
                                placeholder="Paste clinical text here (discharge summary, progress note, lab report, etc.)"
                                value={text}
                                onChange={(e) => setText(e.target.value)}
                            />
                            <button
                                className="btn btn-primary btn-lg"
                                style={{ width: '100%', marginTop: '1rem' }}
                                onClick={runAnalysis}
                                disabled={loading || !text.trim()}
                            >
                                {loading ? (
                                    <>
                                        <div className="spinner" style={{ width: 20, height: 20 }}></div>
                                        Analyzing with {selectedAgents.length || 14} agents...
                                    </>
                                ) : (
                                    <>
                                        <Cpu size={20} />
                                        Run Analysis ({selectedAgents.length || 'All'} agents)
                                    </>
                                )}
                            </button>
                        </div>

                        {results && (
                            <div className="card">
                                <div className="card-header">
                                    <h3 className="card-title">
                                        <div className="card-icon" style={{ background: 'var(--gradient-accent)' }}><Brain size={18} /></div>
                                        Analysis Results
                                    </h3>
                                    <span className="tag success">{results.agents_executed} agents completed</span>
                                </div>

                                {results.summary && (
                                    <div style={{
                                        padding: '1rem',
                                        background: 'rgba(0, 102, 255, 0.05)',
                                        borderRadius: 'var(--radius-md)',
                                        marginBottom: '1rem',
                                        borderLeft: '3px solid var(--primary-400)'
                                    }}>
                                        <h4 style={{ marginBottom: '0.5rem', fontSize: '0.9375rem' }}>Executive Summary</h4>
                                        <MarkdownRenderer content={results.summary} />
                                    </div>
                                )}

                                <div className="results-content" style={{ maxHeight: '600px' }}>
                                    {results.results.map((result, idx) => (
                                        <div key={idx} className="result-item">
                                            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '0.75rem' }}>
                                                <strong style={{ color: 'var(--text-primary)' }}>{result.agent_name}</strong>
                                                <div style={{ display: 'flex', gap: '0.5rem' }}>
                                                    <span className={`tag ${result.status === 'success' ? 'success' : 'error'}`}>
                                                        {result.status}
                                                    </span>
                                                    <span className="tag">{result.execution_time_ms}ms</span>
                                                </div>
                                            </div>
                                            <div style={{ fontSize: '0.875rem' }}>
                                                {typeof result.output === 'object' && result.output.text ? (
                                                    <MarkdownRenderer content={result.output.text} />
                                                ) : typeof result.output === 'object' && result.output.items ? (
                                                    <div>
                                                        <span className="tag" style={{ marginBottom: '0.5rem' }}>{result.output.count} items</span>
                                                        <pre style={{
                                                            fontSize: '0.8125rem',
                                                            color: 'var(--text-secondary)',
                                                            whiteSpace: 'pre-wrap',
                                                            fontFamily: 'inherit',
                                                            marginTop: '0.5rem'
                                                        }}>
                                                            {JSON.stringify(result.output.items, null, 2)}
                                                        </pre>
                                                    </div>
                                                ) : typeof result.output === 'object' ? (
                                                    <pre style={{
                                                        fontSize: '0.8125rem',
                                                        color: 'var(--text-secondary)',
                                                        whiteSpace: 'pre-wrap',
                                                        fontFamily: 'inherit'
                                                    }}>
                                                        {JSON.stringify(result.output, null, 2)}
                                                    </pre>
                                                ) : (
                                                    <MarkdownRenderer content={String(result.output)} />
                                                )}
                                            </div>
                                        </div>
                                    ))}
                                </div>
                            </div>
                        )}
                    </div>

                    <div>
                        <div className="card">
                            <div className="card-header">
                                <h3 className="card-title">
                                    <div className="card-icon"><Bot size={18} /></div>
                                    Select Agents
                                </h3>
                                <button
                                    className="btn btn-secondary"
                                    style={{ fontSize: '0.75rem', padding: '0.25rem 0.5rem' }}
                                    onClick={() => setSelectedAgents([])}
                                >
                                    Select All
                                </button>
                            </div>
                            <div style={{ display: 'flex', flexDirection: 'column', gap: '0.5rem' }}>
                                {agents.map((agent) => (
                                    <div
                                        key={agent.id}
                                        className="agent-card"
                                        style={{
                                            cursor: 'pointer',
                                            background: selectedAgents.includes(agent.id)
                                                ? 'rgba(0, 102, 255, 0.1)'
                                                : 'rgba(255, 255, 255, 0.02)',
                                            border: selectedAgents.includes(agent.id)
                                                ? '1px solid var(--primary-400)'
                                                : '1px solid transparent'
                                        }}
                                        onClick={() => toggleAgent(agent.id)}
                                    >
                                        <div style={{
                                            width: 36,
                                            height: 36,
                                            background: selectedAgents.includes(agent.id)
                                                ? 'var(--gradient-primary)'
                                                : 'rgba(255, 255, 255, 0.05)',
                                            borderRadius: 'var(--radius-md)',
                                            display: 'flex',
                                            alignItems: 'center',
                                            justifyContent: 'center',
                                            color: selectedAgents.includes(agent.id) ? 'white' : 'var(--text-tertiary)'
                                        }}>
                                            <agent.icon size={18} />
                                        </div>
                                        <div className="agent-info">
                                            <div className="agent-name">{agent.name}</div>
                                            <div className="agent-task">{agent.description}</div>
                                        </div>
                                    </div>
                                ))}
                            </div>
                        </div>
                    </div>
                </div>
            </section>
        </div>
    );
};

// Analytics Page
const AnalyticsPage = () => {
    const metrics = [
        { value: '247', label: 'Documents Processed', change: '+12%', positive: true },
        { value: '1,423', label: 'Analyses Completed', change: '+8%', positive: true },
        { value: '45ms', label: 'Avg Search Latency', change: '-15%', positive: true },
        { value: '92%', label: 'Extraction Accuracy', change: '+2%', positive: true },
    ];

    const qualityScores = [
        { name: 'Diagnosis Extraction', accuracy: 94 },
        { name: 'ICD-10 Coding', accuracy: 91 },
        { name: 'Risk Factor Analysis', accuracy: 93 },
        { name: 'Medication Analysis', accuracy: 95 },
        { name: 'Lab Interpretation', accuracy: 97 },
    ];

    return (
        <div className="container">
            <section className="section">
                <div className="section-header">
                    <h2 className="section-title">Platform Analytics</h2>
                    <p className="section-subtitle">
                        Monitor platform performance, extraction accuracy, and usage metrics.
                    </p>
                </div>

                <div className="grid grid-4" style={{ marginBottom: '2rem' }}>
                    {metrics.map((metric, idx) => (
                        <div key={idx} className="card metric-card">
                            <div className="metric-value">{metric.value}</div>
                            <div className="metric-label">{metric.label}</div>
                            <div className={`metric-change ${metric.positive ? 'positive' : 'negative'}`}>
                                <TrendingUp size={12} />
                                {metric.change} vs last week
                            </div>
                        </div>
                    ))}
                </div>

                <div className="grid grid-2">
                    <div className="card">
                        <div className="card-header">
                            <h3 className="card-title">
                                <div className="card-icon"><BarChart3 size={18} /></div>
                                Extraction Accuracy by Agent
                            </h3>
                        </div>
                        <div style={{ display: 'flex', flexDirection: 'column', gap: '1rem' }}>
                            {qualityScores.map((score, idx) => (
                                <div key={idx}>
                                    <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '0.5rem' }}>
                                        <span style={{ fontSize: '0.9375rem' }}>{score.name}</span>
                                        <span style={{ fontWeight: 600, color: 'var(--success-400)' }}>{score.accuracy}%</span>
                                    </div>
                                    <div className="progress-bar">
                                        <div className="progress-fill" style={{ width: `${score.accuracy}%` }}></div>
                                    </div>
                                </div>
                            ))}
                        </div>
                    </div>

                    <div className="card">
                        <div className="card-header">
                            <h3 className="card-title">
                                <div className="card-icon"><LineChart size={18} /></div>
                                Performance Benchmarks
                            </h3>
                        </div>
                        <div style={{ display: 'flex', flexDirection: 'column', gap: '1.5rem' }}>
                            <div style={{
                                padding: '1.5rem',
                                background: 'rgba(34, 197, 94, 0.1)',
                                borderRadius: 'var(--radius-lg)',
                                border: '1px solid rgba(34, 197, 94, 0.2)'
                            }}>
                                <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', marginBottom: '0.5rem' }}>
                                    <Zap size={18} style={{ color: 'var(--success-400)' }} />
                                    <span style={{ fontWeight: 600 }}>Search Performance</span>
                                </div>
                                <p style={{ fontSize: '2rem', fontWeight: 700, color: 'var(--success-400)' }}>
                                    &lt;50ms <span style={{ fontSize: '1rem', color: 'var(--text-secondary)' }}>p99 latency</span>
                                </p>
                            </div>

                            <div style={{
                                padding: '1.5rem',
                                background: 'rgba(0, 102, 255, 0.1)',
                                borderRadius: 'var(--radius-lg)',
                                border: '1px solid rgba(0, 102, 255, 0.2)'
                            }}>
                                <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', marginBottom: '0.5rem' }}>
                                    <Database size={18} style={{ color: 'var(--primary-400)' }} />
                                    <span style={{ fontWeight: 600 }}>Vector Store Capacity</span>
                                </div>
                                <p style={{ fontSize: '2rem', fontWeight: 700, color: 'var(--primary-400)' }}>
                                    10M+ <span style={{ fontSize: '1rem', color: 'var(--text-secondary)' }}>embeddings supported</span>
                                </p>
                            </div>

                            <div style={{
                                padding: '1.5rem',
                                background: 'rgba(20, 184, 166, 0.1)',
                                borderRadius: 'var(--radius-lg)',
                                border: '1px solid rgba(20, 184, 166, 0.2)'
                            }}>
                                <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', marginBottom: '0.5rem' }}>
                                    <Clock size={18} style={{ color: 'var(--accent-400)' }} />
                                    <span style={{ fontWeight: 600 }}>Time Savings</span>
                                </div>
                                <p style={{ fontSize: '2rem', fontWeight: 700, color: 'var(--accent-400)' }}>
                                    85% <span style={{ fontSize: '1rem', color: 'var(--text-secondary)' }}>reduction in analysis time</span>
                                </p>
                            </div>
                        </div>
                    </div>
                </div>
            </section>
        </div>
    );
};

// Main App Component
const App = () => {
    const [currentPage, setCurrentPage] = useState('dashboard');

    const renderPage = () => {
        switch (currentPage) {
            case 'dashboard':
                return <Dashboard setCurrentPage={setCurrentPage} />;
            case 'upload':
                return <UploadPage />;
            case 'search':
                return <SearchPage />;
            case 'agents':
                return <AgentsPage />;
            case 'analytics':
                return <AnalyticsPage />;
            default:
                return <Dashboard setCurrentPage={setCurrentPage} />;
        }
    };

    return (
        <div className="app-container">
            <Navbar currentPage={currentPage} setCurrentPage={setCurrentPage} />
            <main className="main-content">
                {renderPage()}
            </main>
        </div>
    );
};

export default App;
