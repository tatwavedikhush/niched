import { useState } from "react"

function App() {
  const [seed, setSeed] = useState("")
  const [loading, setLoading] = useState(false)
  const [research, setResearch] = useState(null)
  const [generating, setGenerating] = useState(false)
  const [product, setProduct] = useState(null)
  const [generatedFor, setGeneratedFor] = useState(null)
  const [showProduct, setShowProduct] = useState(false)
  const [error, setError] = useState("")
  const [productError, setProductError] = useState("")

  const handleResearch = async () => {
    if (!seed.trim()) return
    setError("")
    setLoading(true)
    setResearch(null)

    try {
      const response = await fetch("http://127.0.0.1:8000/research", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ seed }),
      })

      if (!response.ok) {
        throw new Error("Failed to start research")
      }

      const job = await response.json()

      let result = job

      while (result.status === "running") {
        await new Promise((resolve) => setTimeout(resolve, 2000))

        const statusResponse = await fetch(
          `http://127.0.0.1:8000/research/${job.job_id}`
        )

        if (!statusResponse.ok) {
          throw new Error("Failed to check research status")
        }

        result = await statusResponse.json()
      }

      if (result.status === "failed") {
        throw new Error(result.error || "Research failed")
      }

      setResearch(result)
    } catch (error) {
      console.error(error)
      setError(error.message || "Something went wrong. Please try again.")
    } finally {
      setLoading(false)
    }
  }

  const handleGenerateProduct = async (opportunity) => {
    setProductError("")
    setGenerating(true)
    setProduct(null)
    setGeneratedFor(opportunity.title)

    try {
      const response = await fetch("http://127.0.0.1:8000/products", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(opportunity),
      })

      if (!response.ok) {
        throw new Error("Failed to generate product")
      }

      const data = await response.json()

      setProduct(data)
    } catch (error) {
      console.error(error)
      setProductError(error.message || "Failed to generate product. Please try again.")

    } finally {
      setGenerating(false)
    }
  }

  const opportunities =
    research?.result?.analysis?.opportunities || []

  const painPoints =
    research?.result?.analysis?.pain_points || []

  if (showProduct && product) {
    const generatedProduct = product.product

    return (
      <div className="min-h-screen bg-paper text-ink">

        {/* HEADER */}
        <header className="sticky top-0 z-50 border-b border-border/70 bg-paper/90 backdrop-blur-xl">
          <div className="mx-auto flex h-16 max-w-5xl items-center justify-between px-5">

            <div className="text-sm font-semibold tracking-[0.22em]">
              NICHED
            </div>

            <button
              onClick={() => setShowProduct(false)}
              className="rounded-full border border-border bg-surface px-4 py-2 text-sm font-medium transition hover:border-ink hover:bg-ink hover:text-white"
            >
              ← Back to research
            </button>

          </div>
        </header>

        {/* PRODUCT */}
        <main className="mx-auto max-w-3xl px-5 pb-24 pt-16">

          {/* PRODUCT LABEL */}
          <div className="mb-8 flex items-center gap-2">

            <span className="h-2 w-2 rounded-full bg-accent" />

            <span className="text-[11px] font-semibold tracking-[0.22em] text-muted">
              GENERATED DIGITAL PRODUCT
            </span>

          </div>


          {/* TITLE */}
          <h1 className="font-display text-5xl font-semibold leading-[1.02] tracking-[-0.05em] sm:text-6xl">
            {generatedProduct.title}
          </h1>


          {/* INTRODUCTION */}
          <p className="mt-8 max-w-2xl text-lg leading-8 text-muted">
            {generatedProduct.introduction}
          </p>


          {/* DIVIDER */}
          <div className="my-12 h-px bg-border" />


          {/* SECTIONS */}
          <div className="space-y-12">

            {generatedProduct.sections.map((section, index) => (
              <section key={index}>

                <div className="mb-3 font-mono text-xs text-accent">
                  {String(index + 1).padStart(2, "0")}
                </div>

                <h2 className="font-display text-2xl font-semibold tracking-[-0.025em]">
                  {section.title}
                </h2>

                <p className="mt-4 text-base leading-7 text-muted">
                  {section.content}
                </p>

              </section>
            ))}

          </div>


          {/* CHECKLIST */}
          <section className="mt-16 rounded-2xl border border-border bg-surface p-7">

            <div className="text-[11px] font-semibold tracking-[0.2em] text-muted">
              CHECKLIST
            </div>

            <div className="mt-6 space-y-4">

              {generatedProduct.checklist.map((item, index) => (
                <div
                  key={index}
                  className="flex gap-3 text-sm leading-6"
                >

                  <span className="mt-1 text-accent">
                    ✓
                  </span>

                  <span>
                    {item}
                  </span>

                </div>
              ))}

            </div>

          </section>


          {/* CONCLUSION */}
          <section className="mt-16">

            <div className="text-[11px] font-semibold tracking-[0.2em] text-muted">
              CONCLUSION
            </div>

            <p className="mt-5 text-base leading-7 text-muted">
              {generatedProduct.conclusion}
            </p>

          </section>


          {/* ACTIONS */}
          <div className="mt-14 flex flex-col gap-3 border-t border-border pt-8 sm:flex-row">

            <button
              onClick={() => {
                const filename = product.filename
                window.open(
                  `http://127.0.0.1:8000/products/download/${filename}`,
                  "_blank"
                )
              }}
              className="rounded-full bg-ink px-5 py-2.5 text-sm font-medium text-white transition hover:bg-accent"
            >
              Download PDF ↓
            </button>

            <button
              onClick={() => setShowProduct(false)}
              className="rounded-full border border-border bg-surface px-6 py-3 text-sm font-medium transition hover:border-ink"
            >
              Back to opportunities
            </button>

          </div>

        </main>

      </div>
    )
  }

  return (
    <div className="min-h-screen bg-paper text-ink font-['Inter']">

      {/* NAVBAR */}
      <header className="sticky top-0 z-50 border-b border-border/70 bg-paper/90 backdrop-blur-xl">
        <div className="mx-auto flex h-16 max-w-5xl items-center justify-between px-5">

          <div className="text-sm font-semibold tracking-[0.22em]">
            NICHED
          </div>

          <button
            onClick={() => {
              setSeed("")
              setResearch(null)
            }}
            className="rounded-full border border-border bg-surface px-4 py-2 text-sm font-medium transition hover:border-ink hover:bg-ink hover:text-white"
          >
            + New research
          </button>

        </div>
      </header>


      {/* MAIN CHAT */}
      <main className="mx-auto flex min-h-[calc(100vh-64px)] max-w-3xl flex-col px-5">

        {/* WELCOME */}
        {!research && !loading && (
          <section className="flex flex-1 flex-col justify-center pb-32 pt-16 sm:pt-20">

            {/* Eyebrow */}
            <div className="mb-7 flex items-center gap-2">
              <span className="h-2 w-2 rounded-full bg-accent" />

              <span className="text-[11px] font-semibold tracking-[0.22em] text-muted">
                MARKET INTELLIGENCE
              </span>
            </div>


            {/* Main heading */}
            <h1 className="font-display max-w-3xl text-[3.5rem] font-semibold leading-[0.98] tracking-[-0.055em] sm:text-[4.75rem]">

              Find the next
              <br />

              <span className="relative inline-block">
                opportunity
                <span className="absolute -bottom-1 left-0 h-[3px] w-[72%] rounded-full bg-accent sm:-bottom-2" />
              </span>

              <span className="text-muted">.</span>

            </h1>


            {/* Description */}
            <p className="mt-8 max-w-xl text-[15px] leading-7 text-muted sm:text-[17px]">
              Tell Niched a market, audience or idea.
              <br className="hidden sm:block" />
              We'll find the opportunities hiding inside it.
            </p>


            {/* Examples */}
            <div className="mt-9 flex flex-wrap gap-2">

              <span className="mr-1 self-center text-[11px] font-medium uppercase tracking-wider text-muted">
                Try
              </span>

              {[
                "AI productivity",
                "Indian gaming",
                "Creator economy",
              ].map((example) => (
                <button
                  key={example}
                  onClick={() => setSeed(example)}
                  className="rounded-full border border-border bg-transparent px-4 py-2 text-sm text-muted transition-all duration-200 hover:-translate-y-0.5 hover:border-ink hover:bg-surface hover:text-ink"
                >
                  {example}
                </button>
              ))}

            </div>

          </section>
        )}

        {/* USER MESSAGE */}
        {seed && (loading || research) && (
          <div className="animate-[fadeIn_.3s_ease-out] pt-12">

            <div className="flex justify-end">
              <div className="max-w-[85%] rounded-3xl rounded-br-md bg-ink px-5 py-3.5 text-sm leading-6 text-white">
                {seed}
              </div>
            </div>

          </div>
        )}


        {/* LOADING */}
        {loading && (
          <div className="animate-[fadeIn_.4s_ease-out] py-10">

            <div className="mb-5 text-[11px] font-semibold tracking-[0.2em] text-muted">
              NICHED
            </div>

            <div className="space-y-3">

              <div className="flex items-center gap-3 text-sm text-muted">
                <span className="h-2 w-2 animate-pulse rounded-full bg-accent" />
                Researching Reddit
              </div>

              <div className="flex items-center gap-3 text-sm text-muted">
                <span className="h-2 w-2 animate-pulse rounded-full bg-accent [animation-delay:200ms]" />
                Analyzing Google Trends
              </div>

              <div className="flex items-center gap-3 text-sm text-muted">
                <span className="h-2 w-2 animate-pulse rounded-full bg-accent [animation-delay:400ms]" />
                Finding opportunities
              </div>

            </div>

          </div>
        )}


        {/* RESULTS */}
        {research && !loading && (
          <section className="animate-[fadeIn_.5s_ease-out] pb-56 pt-10">

            {/* ASSISTANT HEADER */}
            <div className="mb-8 flex items-center gap-3">

              <div className="flex h-8 w-8 items-center justify-center rounded-full bg-ink text-[10px] font-bold text-white">
                N
              </div>

              <div>
                <div className="text-sm font-semibold">
                  Niched
                </div>

                <div className="text-xs text-muted">
                  Market research complete
                </div>
              </div>

            </div>


            {/* INTRO */}
            <div className="mb-12">

              <h2 className="text-3xl font-semibold tracking-[-0.03em] sm:text-4xl">
                I found{" "}
                <span className="text-accent">
                  {opportunities.length}
                </span>{" "}
                opportunities worth exploring.
              </h2>

              <p className="mt-4 text-base leading-7 text-muted">
                Based on market signals around{" "}
                <span className="font-medium text-ink">
                  {research.seed}
                </span>
                .
              </p>

            </div>


            {/* PAIN POINTS */}
            <div className="mb-14">

              <div className="mb-4 text-[11px] font-semibold tracking-[0.2em] text-muted">
                PAIN POINTS
              </div>

              <div className="divide-y divide-border border-y border-border">

                {painPoints.map((point, index) => (
                  <div
                    key={index}
                    className="flex gap-5 py-5 transition hover:px-2"
                  >

                    <span className="font-mono text-xs text-accent">
                      {String(index + 1).padStart(2, "0")}
                    </span>

                    <p className="text-sm leading-6 text-ink">
                      {point}
                    </p>

                  </div>
                ))}

              </div>

            </div>

            {productError && (
              <div className="mb-5 rounded-xl border border-red-200 bg-red-50 px-4 py-3 text-sm text-red-700">
                {productError}
              </div>
            )}

            {/* OPPORTUNITIES */}
            <div>

              <div className="mb-5 text-[11px] font-semibold tracking-[0.2em] text-muted">
                OPPORTUNITIES
              </div>

              <div className="space-y-4">

                {opportunities.map((opportunity, index) => (
                  <article
                    key={index}
                    className="group rounded-2xl border border-border bg-surface p-6 transition duration-300 hover:-translate-y-1 hover:border-ink hover:shadow-[0_15px_40px_rgba(0,0,0,0.06)]"
                  >

                    {/* CARD TOP */}
                    <div className="flex items-center justify-between">

                      <span className="font-mono text-xs text-muted">
                        {String(index + 1).padStart(2, "0")}
                      </span>

                      <div className="flex items-center gap-2 text-xs font-medium">
                        <span className="text-muted">
                          DEMAND
                        </span>

                        <span className="text-accent">
                          {opportunity.demand_score}/100
                        </span>
                      </div>

                    </div>


                    {/* TITLE */}
                    <h3 className="mt-6 text-xl font-semibold tracking-[-0.02em]">
                      {opportunity.title}
                    </h3>

                    {/* AUDIENCE */}
                    <p className="mt-2 text-sm font-medium text-accent">
                      {opportunity.target_audience}
                    </p>

                    {/* PROBLEM */}
                    <p className="mt-4 text-sm leading-6 text-muted">
                      {opportunity.problem}
                    </p>


                    {/* DEMAND BAR */}
                    <div className="mt-6 h-1.5 overflow-hidden rounded-full bg-border">

                      <div
                        className="h-full rounded-full bg-accent transition-all duration-700"
                        style={{
                          width: `${opportunity.demand_score}%`,
                        }}
                      />

                    </div>


                    {/* FOOTER */}
                    <div className="mt-6 flex flex-col gap-4 border-t border-border pt-5 sm:flex-row sm:items-center sm:justify-between">

                      <span className="text-sm font-medium">
                        {opportunity.suggested_price}
                      </span>

                      {product && generatedFor === opportunity.title ? (
                        <div className="flex items-center gap-3">
                          <span className="text-sm font-medium text-accent">
                            ✓ Product ready
                          </span>

                          <button
                            onClick={() => setShowProduct(true)}
                            className="rounded-full bg-ink px-5 py-2.5 text-sm font-medium text-white transition hover:bg-accent"
                          >
                            View product →
                          </button>
                        </div>
                      ) : (
                        <button
                          onClick={() => handleGenerateProduct(opportunity)}
                          disabled={generating}
                          className="group/btn flex items-center justify-center gap-2 rounded-full bg-ink px-5 py-2.5 text-sm font-medium text-white transition hover:bg-accent disabled:cursor-not-allowed disabled:opacity-60"
                        >
                          {generating ? "Generating..." : "Generate product"}

                          {!generating && (
                            <span className="transition-transform group-hover/btn:translate-x-1">
                              →
                            </span>
                          )}
                        </button>
                      )}

                    </div>

                  </article>
                ))}

              </div>

            </div>

          </section>
        )}


        {/* COMPOSER */}
        <div className="fixed bottom-5 left-1/2 z-40 w-[calc(100%-32px)] max-w-3xl -translate-x-1/2">

          <div className="flex items-center gap-2 rounded-2xl border border-border bg-surface/95 p-2 shadow-[0_10px_40px_rgba(0,0,0,0.08)] backdrop-blur-xl">

            <input
              value={seed}
              onChange={(e) => setSeed(e.target.value)}
              onKeyDown={(e) => {
                if (e.key === "Enter") {
                  handleResearch()
                }
              }}
              placeholder="Explore a market or idea..."
              disabled={loading}
              className="min-w-0 flex-1 bg-transparent px-4 py-3 text-sm outline-none placeholder:text-muted disabled:opacity-50"
            />

            <button
              onClick={handleResearch}
              disabled={loading || !seed.trim()}
              className={`flex h-11 w-11 shrink-0 items-center justify-center rounded-xl text-lg text-white transition-all duration-200 ${seed.trim() && !loading
                ? "bg-accent hover:-translate-y-0.5 hover:bg-accent-dark hover:shadow-lg"
                : "bg-ink/20 cursor-not-allowed"
                }`}
            >
              {loading ? (
                <span className="h-4 w-4 animate-spin rounded-full border-2 border-white/40 border-t-white" />
              ) : (
                "↑"
              )}
            </button>

          </div>
          {error && (
            <div className="mt-3 rounded-xl border border-red-200 bg-red-50 px-4 py-3 text-sm text-red-700 shadow-sm">
              {error}
            </div>
          )}
          <p className="mt-2 text-center text-[10px] tracking-wide text-muted/70">
            Reddit signals · Google Trends · AI analysis
          </p>

        </div>

      </main>

    </div>
  )
}

export default App