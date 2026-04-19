import { useState, useEffect } from "react"
import axios from "axios"
import { BarChart, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer, Cell } from "recharts"

const API = import.meta.env.VITE_API_URL || "http://localhost:8000"

const STATE_COLORS = {
  "Stable": "#4ade80",
  "Political Tension": "#a3e635",
  "Diplomatic Conflict": "#facc15",
  "Military Posturing": "#fb923c",
  "Limited Conflict": "#f87171",
  "Full Escalation": "#ef4444",
}

const THREAT_LEVEL = (avg) => {
  if (avg < 1) return { label: "MINIMAL", color: "#4ade80" }
  if (avg < 2) return { label: "LOW", color: "#a3e635" }
  if (avg < 3) return { label: "ELEVATED", color: "#facc15" }
  if (avg < 4) return { label: "HIGH", color: "#fb923c" }
  return { label: "CRITICAL", color: "#ef4444" }
}

function ScanlineOverlay() {
  return (
    <div style={{
      position: "fixed", inset: 0, pointerEvents: "none", zIndex: 0,
      backgroundImage: "repeating-linear-gradient(0deg, transparent, transparent 2px, rgba(0,0,0,0.03) 2px, rgba(0,0,0,0.03) 4px)",
    }} />
  )
}

function GridBackground() {
  return (
    <div style={{
      position: "fixed", inset: 0, pointerEvents: "none", zIndex: 0,
      backgroundImage: `
        linear-gradient(rgba(255,59,59,0.03) 1px, transparent 1px),
        linear-gradient(90deg, rgba(255,59,59,0.03) 1px, transparent 1px)
      `,
      backgroundSize: "40px 40px",
    }} />
  )
}

function Ticker() {
  const items = [
    "MONTE CARLO ENGINE ACTIVE",
    "NEWSAPI FEED CONNECTED",
    "CLAUDE AI EXTRACTION ONLINE",
    "AUTO STATE DETECTION ENABLED",
    "HYPOTHETICAL SCENARIO MODELING",
    "6 ESCALATION STATES MODELED",
  ]
  const [pos, setPos] = useState(0)
  useEffect(() => {
    const interval = setInterval(() => setPos(p => p - 1), 30)
    return () => clearInterval(interval)
  }, [])

  const fullText = items.join("   ///   ") + "   ///   "
  const charWidth = 8.4
  const totalWidth = fullText.length * charWidth
  const wrappedPos = ((pos % totalWidth) + totalWidth) % totalWidth

  return (
    <div style={{
      borderTop: "1px solid rgba(255,59,59,0.2)",
      borderBottom: "1px solid rgba(255,59,59,0.2)",
      background: "rgba(255,59,59,0.04)",
      padding: "6px 0", overflow: "hidden", whiteSpace: "nowrap",
    }}>
      <span style={{
        display: "inline-block",
        transform: `translateX(-${wrappedPos}px)`,
        fontFamily: "'Courier New', monospace",
        fontSize: 11, color: "rgba(255,59,59,0.6)",
        letterSpacing: "0.08em",
      }}>
        {fullText.repeat(3)}
      </span>
    </div>
  )
}

export default function App() {
  const [mode, setMode] = useState("live")
  const [conflict, setConflict] = useState("")
  const [scenarios, setScenarios] = useState([""])
  const [loading, setLoading] = useState(false)
  const [results, setResults] = useState(null)
  const [error, setError] = useState(null)
  const [dots, setDots] = useState("")

  useEffect(() => {
    if (!loading) return
    const i = setInterval(() => setDots(d => d.length >= 3 ? "" : d + "."), 400)
    return () => clearInterval(i)
  }, [loading])

  const addScenario = () => setScenarios([...scenarios, ""])
  const removeScenario = (idx) => setScenarios(scenarios.filter((_, i) => i !== idx))
  const updateScenario = (idx, value) => {
    const next = [...scenarios]
    next[idx] = value
    setScenarios(next)
  }

  const runSimulation = async () => {
    if (!conflict.trim()) { setError("// ERROR: CONFLICT IDENTIFIER REQUIRED"); return }

    if (mode === "manual") {
      const filled = scenarios.filter(s => s.trim()).join("\n\n")
      if (!filled) { setError("// ERROR: AT LEAST ONE SCENARIO REQUIRED"); return }
    }

    setLoading(true); setError(null); setResults(null)
    try {
      const endpoint = mode === "live" ? "/simulate/live" : "/simulate/hypothetical"
      const payload = mode === "live"
        ? { conflict, turns: 10, num_simulations: 1000 }
        : {
            conflict,
            scenario_description: scenarios.filter(s => s.trim()).join("\n\n"),
            turns: 10,
            num_simulations: 1000,
          }
      const response = await axios.post(`${API}${endpoint}`, payload)
      setResults(response.data)
    } catch (err) {
      setError(`// ERROR: ${err.response?.data?.detail || "BACKEND UNREACHABLE"}`)
    } finally {
      setLoading(false)
    }
  }

  const chartData = results
    ? Object.entries(results.simulation.outcome_probabilities)
        .map(([name, probability]) => ({ name, probability }))
        .sort((a, b) => b.probability - a.probability)
    : []

  const threat = results ? THREAT_LEVEL(results.simulation.average_final_level) : null

  const css = `
    @import url('https://fonts.googleapis.com/css2?family=Share+Tech+Mono&family=Bebas+Neue&family=IBM+Plex+Mono:wght@300;400;500&display=swap');
    * { margin: 0; padding: 0; box-sizing: border-box; }
    body { background: #080b0f; }
    ::selection { background: rgba(255,59,59,0.3); }
    ::-webkit-scrollbar { width: 4px; }
    ::-webkit-scrollbar-track { background: #080b0f; }
    ::-webkit-scrollbar-thumb { background: rgba(255,59,59,0.3); border-radius: 2px; }
    input, select, textarea { outline: none; }
    input::placeholder, textarea::placeholder { color: rgba(255,255,255,0.15); }
    @keyframes fadeUp {
      from { opacity: 0; transform: translateY(16px); }
      to { opacity: 1; transform: translateY(0); }
    }
    @keyframes pulse-red {
      0%, 100% { box-shadow: 0 0 0 0 rgba(255,59,59,0.4); }
      50% { box-shadow: 0 0 0 6px rgba(255,59,59,0); }
    }
    .fade-up { animation: fadeUp 0.5s ease forwards; }
    .fade-up-1 { animation: fadeUp 0.5s 0.1s ease both; }
    .fade-up-2 { animation: fadeUp 0.5s 0.2s ease both; }
    .fade-up-3 { animation: fadeUp 0.5s 0.3s ease both; }
    .run-btn:hover:not(:disabled) { background: rgba(255,59,59,0.15) !important; border-color: rgba(255,59,59,0.8) !important; }
    .mode-btn:hover { background: rgba(255,255,255,0.05) !important; }
    .add-btn:hover { border-color: rgba(255,59,59,0.5) !important; color: #ff6b6b !important; }
    .remove-btn:hover { color: #ff6b6b !important; }
  `

  return (
    <>
      <style>{css}</style>
      <ScanlineOverlay />
      <GridBackground />

      <div style={{ position: "relative", zIndex: 1, minHeight: "100vh", color: "#c8d0dc", fontFamily: "'IBM Plex Mono', monospace" }}>

        {/* Header */}
        <div style={{ borderBottom: "1px solid rgba(255,59,59,0.15)", padding: "20px 40px", display: "flex", alignItems: "center", justifyContent: "space-between" }}>
          <div>
            <div style={{ fontFamily: "'Bebas Neue', sans-serif", fontSize: 36, letterSpacing: "0.12em", color: "#fff", lineHeight: 1 }}>
              CRISISSIM
            </div>
            <div style={{ fontSize: 10, color: "rgba(255,59,59,0.6)", letterSpacing: "0.2em", marginTop: 4 }}>
              GEOPOLITICAL ESCALATION ANALYSIS SYSTEM
            </div>
          </div>
          <div style={{ textAlign: "right" }}>
            <div style={{ fontSize: 10, color: "rgba(255,255,255,0.2)", letterSpacing: "0.15em" }}>STATUS</div>
            <div style={{ fontSize: 12, color: "#4ade80", letterSpacing: "0.1em", display: "flex", alignItems: "center", gap: 6, justifyContent: "flex-end" }}>
              <span style={{ width: 6, height: 6, borderRadius: "50%", background: "#4ade80", display: "inline-block", animation: "pulse-red 2s infinite" }} />
              ONLINE
            </div>
          </div>
        </div>

        <Ticker />

        <div style={{ maxWidth: 1100, margin: "0 auto", padding: "40px 24px" }}>

          {/* Mode Toggle */}
          <div style={{ display: "flex", gap: 2, marginBottom: 32, background: "rgba(255,255,255,0.03)", borderRadius: 6, padding: 3, width: "fit-content", border: "1px solid rgba(255,255,255,0.06)" }}>
            {[
              { id: "live", label: "// LIVE INTEL" },
              { id: "manual", label: "// HYPOTHETICAL" },
            ].map(m => (
              <button key={m.id} className="mode-btn" onClick={() => { setMode(m.id); setResults(null); setError(null) }} style={{
                padding: "7px 18px", borderRadius: 4, border: "none", cursor: "pointer",
                fontFamily: "'Share Tech Mono', monospace", fontSize: 12, letterSpacing: "0.08em",
                background: mode === m.id ? "rgba(255,59,59,0.15)" : "transparent",
                color: mode === m.id ? "#ff6b6b" : "rgba(255,255,255,0.3)",
                transition: "all 0.2s",
              }}>
                {m.label}
              </button>
            ))}
          </div>

          <div style={{ display: "grid", gridTemplateColumns: results ? "1fr 1fr" : "1fr", gap: 24, transition: "all 0.3s" }}>

            {/* Input Panel */}
            <div className="fade-up" style={{ border: "1px solid rgba(255,255,255,0.07)", borderRadius: 8, overflow: "hidden", background: "rgba(255,255,255,0.02)" }}>

              <div style={{ padding: "12px 20px", borderBottom: "1px solid rgba(255,255,255,0.06)", background: "rgba(255,59,59,0.05)", display: "flex", alignItems: "center", gap: 8 }}>
                <span style={{ width: 6, height: 6, borderRadius: "50%", background: "rgba(255,59,59,0.8)" }} />
                <span style={{ fontSize: 11, letterSpacing: "0.15em", color: "rgba(255,255,255,0.4)" }}>SIMULATION INPUT</span>
              </div>

              <div style={{ padding: 24 }}>

                {/* Conflict Input */}
                <div style={{ marginBottom: 20 }}>
                  <div style={{ fontSize: 10, color: "rgba(255,59,59,0.6)", letterSpacing: "0.2em", marginBottom: 8 }}>TARGET CONFLICT</div>
                  <div style={{ position: "relative" }}>
                    <input
                      type="text"
                      value={conflict}
                      onChange={e => setConflict(e.target.value)}
                      placeholder={mode === "live" ? "e.g. Russia Ukraine" : "e.g. Taiwan Strait"}
                      style={{
                        width: "100%", padding: "11px 14px 11px 32px",
                        background: "rgba(0,0,0,0.4)", border: "1px solid rgba(255,255,255,0.08)",
                        borderRadius: 6, color: "#e2e8f0", fontSize: 14,
                        fontFamily: "'Share Tech Mono', monospace", letterSpacing: "0.05em",
                        transition: "border-color 0.2s",
                      }}
                      onFocus={e => e.target.style.borderColor = "rgba(255,59,59,0.4)"}
                      onBlur={e => e.target.style.borderColor = "rgba(255,255,255,0.08)"}
                    />
                    <span style={{ position: "absolute", left: 12, top: "50%", transform: "translateY(-50%)", fontSize: 12, color: "rgba(255,59,59,0.4)", fontFamily: "monospace" }}>›</span>
                  </div>
                </div>

                {/* Mode Description */}
                {mode === "live" && (
                  <div style={{ marginBottom: 20, padding: "10px 14px", background: "rgba(74,222,128,0.04)", border: "1px solid rgba(74,222,128,0.15)", borderRadius: 6, fontSize: 11, color: "rgba(74,222,128,0.7)", lineHeight: 1.6 }}>
                    // AI WILL AUTO-DETECT CURRENT STATE AND EVENTS FROM LIVE NEWS
                  </div>
                )}

                {/* Hypothetical Scenarios */}
                {mode === "manual" && (
                  <div style={{ marginBottom: 20 }}>
                    <div style={{ fontSize: 10, color: "rgba(255,59,59,0.6)", letterSpacing: "0.2em", marginBottom: 10 }}>HYPOTHETICAL SCENARIOS</div>
                    <div style={{ display: "flex", flexDirection: "column", gap: 8 }}>
                      {scenarios.map((scenario, idx) => (
                        <div key={idx} style={{ display: "flex", gap: 8, alignItems: "flex-start" }}>
                          <textarea
                            value={scenario}
                            onChange={e => updateScenario(idx, e.target.value)}
                            placeholder={idx === 0 ? "e.g. China deploys troops to disputed islands" : "Additional scenario..."}
                            rows={2}
                            style={{
                              flex: 1, padding: "10px 14px",
                              background: "rgba(0,0,0,0.4)", border: "1px solid rgba(255,255,255,0.08)",
                              borderRadius: 6, color: "#e2e8f0", fontSize: 13,
                              fontFamily: "'Share Tech Mono', monospace", letterSpacing: "0.03em",
                              lineHeight: 1.5, resize: "vertical",
                              transition: "border-color 0.2s",
                            }}
                            onFocus={e => e.target.style.borderColor = "rgba(255,59,59,0.4)"}
                            onBlur={e => e.target.style.borderColor = "rgba(255,255,255,0.08)"}
                          />
                          {scenarios.length > 1 && (
                            <button className="remove-btn" onClick={() => removeScenario(idx)} style={{
                              padding: "0 10px", background: "transparent", border: "1px solid rgba(255,255,255,0.08)",
                              borderRadius: 6, color: "rgba(255,255,255,0.3)", cursor: "pointer",
                              fontSize: 16, fontFamily: "monospace", alignSelf: "stretch",
                              transition: "color 0.2s",
                            }}>×</button>
                          )}
                        </div>
                      ))}
                      <button className="add-btn" onClick={addScenario} style={{
                        padding: "8px", background: "transparent",
                        border: "1px dashed rgba(255,255,255,0.15)",
                        borderRadius: 6, color: "rgba(255,255,255,0.35)", cursor: "pointer",
                        fontSize: 12, fontFamily: "'Share Tech Mono', monospace", letterSpacing: "0.1em",
                        transition: "all 0.2s",
                      }}>
                        + ADD SCENARIO
                      </button>
                    </div>
                    <div style={{ marginTop: 10, fontSize: 10, color: "rgba(255,255,255,0.25)", lineHeight: 1.6, letterSpacing: "0.05em" }}>
                      // AI WILL INFER CURRENT STATE AND MAP SCENARIOS TO EVENTS
                    </div>
                  </div>
                )}

                {/* Run Button */}
                <button className="run-btn" onClick={runSimulation} disabled={loading} style={{
                  width: "100%", padding: "13px",
                  background: "rgba(255,59,59,0.08)",
                  border: "1px solid rgba(255,59,59,0.4)",
                  borderRadius: 6, color: loading ? "rgba(255,107,107,0.5)" : "#ff6b6b",
                  fontSize: 13, fontWeight: 600, cursor: loading ? "not-allowed" : "pointer",
                  fontFamily: "'Share Tech Mono', monospace", letterSpacing: "0.15em",
                  transition: "all 0.2s",
                }}>
                  {loading ? `PROCESSING${dots}` : "▶  EXECUTE SIMULATION"}
                </button>

                {error && (
                  <div style={{ marginTop: 12, padding: "10px 14px", background: "rgba(255,59,59,0.05)", border: "1px solid rgba(255,59,59,0.2)", borderRadius: 6, fontSize: 12, color: "#f87171", fontFamily: "monospace" }}>
                    {error}
                  </div>
                )}
              </div>
            </div>

            {/* Results Panel */}
            {results && (
              <div style={{ display: "flex", flexDirection: "column", gap: 16 }}>

                {/* Threat Level */}
                <div className="fade-up-1" style={{ border: `1px solid ${threat.color}30`, borderRadius: 8, padding: "16px 20px", background: `${threat.color}08`, display: "flex", alignItems: "center", justifyContent: "space-between" }}>
                  <div>
                    <div style={{ fontSize: 10, color: "rgba(255,255,255,0.3)", letterSpacing: "0.2em", marginBottom: 4 }}>THREAT ASSESSMENT</div>
                    <div style={{ fontFamily: "'Bebas Neue', sans-serif", fontSize: 32, color: threat.color, letterSpacing: "0.1em", lineHeight: 1 }}>{threat.label}</div>
                  </div>
                  <div style={{ textAlign: "right" }}>
                    <div style={{ fontSize: 10, color: "rgba(255,255,255,0.3)", letterSpacing: "0.15em", marginBottom: 4 }}>AVG LEVEL</div>
                    <div style={{ fontFamily: "'Bebas Neue', sans-serif", fontSize: 40, color: threat.color, lineHeight: 1 }}>{results.simulation.average_final_level}<span style={{ fontSize: 18, opacity: 0.5 }}>/5</span></div>
                  </div>
                </div>

                {/* AI Assessment */}
                <div className="fade-up-2" style={{ border: "1px solid rgba(255,255,255,0.07)", borderRadius: 8, padding: "14px 20px", background: "rgba(255,255,255,0.02)" }}>
                  <div style={{ fontSize: 10, color: "rgba(255,59,59,0.6)", letterSpacing: "0.2em", marginBottom: 12 }}>AI ASSESSMENT</div>

                  <div style={{ fontSize: 11, color: "rgba(255,255,255,0.4)", marginBottom: 6, letterSpacing: "0.05em" }}>DETECTED STARTING STATE:</div>
                  <div style={{ fontSize: 14, color: "#e2e8f0", marginBottom: 14, fontFamily: "'Share Tech Mono', monospace" }}>
                    [{results.detected_starting_state_level}] {results.detected_starting_state.toUpperCase()}
                  </div>

                  <div style={{ fontSize: 11, color: "rgba(255,255,255,0.4)", marginBottom: 8, letterSpacing: "0.05em" }}>ACTIVE EVENTS:</div>
                  {results.detected_events?.length > 0 ? (
                    <div style={{ display: "flex", flexWrap: "wrap", gap: 6, marginBottom: 10 }}>
                      {results.detected_events.map(e => (
                        <span key={e} style={{ padding: "3px 10px", borderRadius: 3, background: "rgba(255,59,59,0.1)", border: "1px solid rgba(255,59,59,0.25)", fontSize: 11, color: "#ff6b6b", fontFamily: "monospace" }}>
                          {e.replace(/_/g, " ").toUpperCase()}
                        </span>
                      ))}
                    </div>
                  ) : (
                    <div style={{ fontSize: 12, color: "rgba(255,255,255,0.3)", fontStyle: "italic", marginBottom: 10 }}>None detected</div>
                  )}

                  {results.ai_confidence && (
                    <div style={{ fontSize: 11, color: "rgba(255,255,255,0.3)", fontFamily: "monospace" }}>
                      CONFIDENCE: <span style={{ color: results.ai_confidence === "high" ? "#4ade80" : results.ai_confidence === "medium" ? "#facc15" : "#f87171" }}>{results.ai_confidence.toUpperCase()}</span>
                    </div>
                  )}
                </div>

                {/* Chart */}
                <div className="fade-up-2" style={{ border: "1px solid rgba(255,255,255,0.07)", borderRadius: 8, padding: "16px 20px", background: "rgba(255,255,255,0.02)", flex: 1 }}>
                  <div style={{ fontSize: 10, color: "rgba(255,59,59,0.6)", letterSpacing: "0.2em", marginBottom: 16 }}>OUTCOME PROBABILITY DISTRIBUTION</div>
                  <ResponsiveContainer width="100%" height={220}>
                    <BarChart data={chartData} layout="vertical" margin={{ left: 10, right: 50, top: 0, bottom: 0 }}>
                      <XAxis type="number" domain={[0, 100]} tick={{ fill: "rgba(255,255,255,0.2)", fontSize: 10, fontFamily: "monospace" }} tickFormatter={v => `${v}%`} axisLine={false} tickLine={false} />
                      <YAxis type="category" dataKey="name" tick={{ fill: "rgba(255,255,255,0.4)", fontSize: 11, fontFamily: "monospace" }} width={155} axisLine={false} tickLine={false} />
                      <Tooltip
                        formatter={v => [`${v}%`, "Probability"]}
                        contentStyle={{ background: "#0d1117", border: "1px solid rgba(255,59,59,0.2)", borderRadius: 6, fontFamily: "monospace", fontSize: 12 }}
                        labelStyle={{ color: "rgba(255,255,255,0.6)" }}
                        cursor={{ fill: "rgba(255,255,255,0.02)" }}
                      />
                      <Bar dataKey="probability" radius={[0, 3, 3, 0]} label={{ position: "right", fill: "rgba(255,255,255,0.3)", fontSize: 11, fontFamily: "monospace", formatter: v => `${v}%` }}>
                        {chartData.map(entry => (
                          <Cell key={entry.name} fill={STATE_COLORS[entry.name] || "#ff6b6b"} opacity={0.85} />
                        ))}
                      </Bar>
                    </BarChart>
                  </ResponsiveContainer>
                </div>

                {/* Trajectory */}
                <div className="fade-up-3" style={{ border: "1px solid rgba(255,255,255,0.07)", borderRadius: 8, padding: "14px 20px", background: "rgba(255,255,255,0.02)" }}>
                  <div style={{ fontSize: 10, color: "rgba(255,59,59,0.6)", letterSpacing: "0.2em", marginBottom: 8 }}>MOST PROBABLE TRAJECTORY</div>
                  <div style={{ fontSize: 12, color: "rgba(255,255,255,0.5)", lineHeight: 1.7, fontFamily: "'Share Tech Mono', monospace" }}>
                    {results.simulation.most_common_trajectory}
                  </div>
                </div>

              </div>
            )}
          </div>
        </div>
      </div>
    </>
  )
}