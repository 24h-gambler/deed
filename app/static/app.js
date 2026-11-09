const krw = new Intl.NumberFormat("ko-KR");
const $ = (id) => document.getElementById(id);

let currentRequestId = null;

function money(value) {
  return krw.format(Math.round(Number(value) || 0)) + "원";
}

function escapeHtml(value) {
  return String(value == null ? "" : value).replace(/[&<>"']/g, (c) => ({
    "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;",
  }[c]));
}

function setError(message) {
  const el = $("error");
  if (!message) {
    el.hidden = true;
    el.textContent = "";
    return;
  }
  el.hidden = false;
  el.textContent = message;
}

async function api(path, options = {}) {
  const response = await fetch(path, {
    headers: { "Content-Type": "application/json" },
    ...options,
  });
  const data = await response.json();
  if (!response.ok) throw new Error(data.error || "Request failed");
  return data;
}

async function loadStats() {
  const s = await api("/api/stats");
  $("stat-requests").textContent = s.requests;
  $("stat-submissions").textContent = s.submissions;
  $("stat-accepted").textContent = s.accepted;
  $("stat-assets").textContent = s.assets;
  $("stat-gmv").textContent = money(s.gross_krw);
  $("stat-creator").textContent = money(s.creator_paid_krw);
  $("stat-platform").textContent = money(s.platform_revenue_krw);
}

async function loadAssets() {
  const data = await api("/api/assets");
  const box = $("catalog");
  if (!data.assets.length) {
    box.innerHTML = `<div class="empty">No data listed yet. Upload the first one.</div>`;
    return;
  }
  box.innerHTML = data.assets
    .map(
      (a) => `
      <div class="asset-card">
        <div class="asset-head">
          <span class="type-badge">${escapeHtml(a.data_type)}</span>
          <span class="score ${a.qc_score < 0.8 ? "low" : ""}">QC ${a.qc_score.toFixed(2)}</span>
        </div>
        <h4>${escapeHtml(a.title)}</h4>
        <p>${escapeHtml(a.creator)} · ${escapeHtml(a.domain)}</p>
        <p class="asset-desc">${escapeHtml(a.description || "")}</p>
        <div class="asset-foot">
          <strong>${money(a.price_krw)}</strong>
          <span class="status-pill ${a.status === "LICENSED" ? "licensed" : ""}">${escapeHtml(a.status)}</span>
        </div>
        ${
          a.status === "LISTED"
            ? `<button class="secondary license-asset" data-asset="${a.id}">License</button>`
            : ""
        }
      </div>`
    )
    .join("");
}

async function loadRequests() {
  const data = await api("/api/requests");
  const list = $("request-list");
  if (!data.requests.length) {
    list.innerHTML = `<div class="empty">No requests yet. Post one above.</div>`;
    return;
  }
  list.innerHTML = data.requests
    .map(
      (r) => `
      <div class="request-item ${r.id === currentRequestId ? "active" : ""}" data-id="${r.id}">
        <h4>${escapeHtml(r.title)}</h4>
        <p>${escapeHtml(r.buyer)} · ${escapeHtml(r.domain)}</p>
        <div class="request-meta">
          <span>${money(r.unit_price_krw)} / unit</span>
          <span>${r.accepted_count}/${r.submission_count} accepted</span>
        </div>
      </div>`
    )
    .join("");
}

function renderSubmissions(request) {
  const box = $("submissions");
  if (!request.submissions.length) {
    box.innerHTML = `<div class="empty">No submissions yet.</div>`;
    return;
  }
  box.innerHTML = request.submissions
    .map((s) => {
      const actions =
        s.status === "PENDING"
          ? `<div class="sub-actions">
               <button class="accept" data-submission="${s.id}" data-action="accept">Accept</button>
               <button class="reject" data-submission="${s.id}" data-action="reject">Reject</button>
             </div>`
          : "";
      return `
        <div class="submission">
          <div class="submission-head">
            <div>
              <h4>${escapeHtml(s.creator)} · ${escapeHtml(s.file_name)}</h4>
              <p>${escapeHtml(s.note || "no note")}</p>
            </div>
            <span class="score ${s.qc_score < 0.8 ? "low" : ""}">QC ${s.qc_score.toFixed(2)}</span>
          </div>
          <div class="request-meta"><span>${escapeHtml(s.status)}</span><span>${s.created_at}</span></div>
          ${actions}
        </div>`;
    })
    .join("");
}

async function selectRequest(id) {
  currentRequestId = id;
  const request = await api(`/api/requests/${id}`);
  $("detail-empty").hidden = true;
  $("detail").hidden = false;
  $("detail-title").textContent = request.title;
  $("detail-meta").textContent = `${request.buyer} · ${request.domain} · deadline ${request.deadline || "—"}`;
  $("detail-status").textContent = request.status;
  $("detail-status").className = "status-pill " + (request.status === "LICENSED" ? "licensed" : "");
  $("detail-spec").textContent = request.spec;
  $("detail-rate").textContent = money(request.unit_price_krw) + " / unit";
  $("detail-qty").textContent = request.quantity;
  $("detail-accepted").textContent = request.submissions.filter((s) => s.status === "ACCEPTED").length;
  $("detail-rights").textContent = request.rights;

  renderSubmissions(request);

  const licensed = request.status === "LICENSED";
  $("submit-box").hidden = licensed;
  $("license").disabled = licensed;
  $("license").textContent = licensed ? "Licensed" : "License dataset";
  if (!licensed) $("license-result").hidden = true;

  await loadRequests();
}

async function loadLedger() {
  const data = await api("/api/ledger");
  $("balance").textContent = data.balanced
    ? `Balanced · ${money(data.total_debit)}`
    : `UNBALANCED · Dr ${money(data.total_debit)} / Cr ${money(data.total_credit)}`;
  $("balance").classList.toggle("bad", !data.balanced);

  $("accounts").innerHTML = data.accounts
    .map(
      (a) => `<tr><td>${escapeHtml(a.account)}</td><td class="num">${money(a.debit)}</td><td class="num">${money(
        a.credit
      )}</td></tr>`
    )
    .join("");

  if (!data.entries.length) {
    $("entries").innerHTML = `<div class="empty">No entries yet. License a dataset.</div>`;
    return;
  }

  $("entries").innerHTML = data.entries
    .slice()
    .reverse()
    .map((e) => {
      const rows = e.postings
        .map(
          (p) =>
            `<tr><td>${escapeHtml(p.account)}</td><td>${money(p.debit)}</td><td>${money(p.credit)}</td></tr>`
        )
        .join("");
      return `
        <div class="entry">
          <div class="entry-head"><span>${e.source_type}</span><span>${e.source_id}</span></div>
          <table>
            <thead><tr><th>Account</th><th>Debit</th><th>Credit</th></tr></thead>
            <tbody>${rows}</tbody>
          </table>
        </div>`;
    })
    .join("");
}

$("asset-form").addEventListener("submit", async (event) => {
  event.preventDefault();
  setError("");
  try {
    await api("/api/assets", {
      method: "POST",
      body: JSON.stringify({
        creator: $("asset-creator").value,
        title: $("asset-title").value,
        data_type: $("asset-type").value,
        domain: $("asset-domain").value,
        description: $("asset-description").value,
        file_name: $("asset-file").value,
        price_krw: Number($("asset-price").value),
      }),
    });
    await loadAssets();
    await loadStats();
  } catch (error) {
    setError(error.message);
  }
});

$("catalog").addEventListener("click", async (event) => {
  const button = event.target.closest("button[data-asset]");
  if (!button) return;
  setError("");
  try {
    await api(`/api/assets/${button.dataset.asset}/license`, {
      method: "POST",
      body: JSON.stringify({ buyer: "Catalog Buyer" }),
    });
    await loadAssets();
    await loadStats();
    await loadLedger();
  } catch (error) {
    setError(error.message);
  }
});

$("request-form").addEventListener("submit", async (event) => {
  event.preventDefault();
  setError("");
  try {
    const request = await api("/api/requests", {
      method: "POST",
      body: JSON.stringify({
        buyer: $("buyer").value,
        title: $("title").value,
        domain: $("domain").value,
        spec: $("spec").value,
        quantity: Number($("quantity").value),
        unit_price_krw: Number($("unit-price").value),
        rights: $("rights").value,
        deadline: $("deadline").value,
      }),
    });
    await loadStats();
    await loadRequests();
    await selectRequest(request.id);
  } catch (error) {
    setError(error.message);
  }
});

$("request-list").addEventListener("click", async (event) => {
  const item = event.target.closest(".request-item");
  if (!item) return;
  try {
    await selectRequest(item.dataset.id);
  } catch (error) {
    setError(error.message);
  }
});

$("submit-form").addEventListener("submit", async (event) => {
  event.preventDefault();
  if (!currentRequestId) return;
  setError("");
  try {
    await api(`/api/requests/${currentRequestId}/submissions`, {
      method: "POST",
      body: JSON.stringify({
        creator: $("creator").value,
        file_name: $("file-name").value,
        note: $("note").value,
      }),
    });
    await selectRequest(currentRequestId);
    await loadStats();
  } catch (error) {
    setError(error.message);
  }
});

$("submissions").addEventListener("click", async (event) => {
  const button = event.target.closest("button[data-submission]");
  if (!button) return;
  try {
    await api(`/api/submissions/${button.dataset.submission}/${button.dataset.action}`, {
      method: "POST",
      body: JSON.stringify({}),
    });
    await selectRequest(currentRequestId);
    await loadStats();
  } catch (error) {
    setError(error.message);
  }
});

$("license").addEventListener("click", async () => {
  if (!currentRequestId) return;
  setError("");
  try {
    const result = await api(`/api/requests/${currentRequestId}/license`, {
      method: "POST",
      body: JSON.stringify({}),
    });
    $("license-result").hidden = false;
    $("license-result").textContent =
      `Licensed ${result.licensed_units} units · GMV ${money(result.gross_krw)} · ` +
      `creator ${money(result.creator_share_krw)} · platform ${money(result.platform_share_krw)}`;
    await selectRequest(currentRequestId);
    await loadStats();
    await loadLedger();
  } catch (error) {
    setError(error.message);
  }
});

(async function init() {
  try {
    await loadStats();
    await loadAssets();
    await loadRequests();
    await loadLedger();
  } catch (error) {
    setError(error.message);
  }
})();
