const SKIP = new Set([
  "letter", "image_meta", "compute", "validation_errors", "schema_title",
  "offline", "device_target", "extraction_mode", "source_image"
]);

let current = null;

function renderFields(record) {
  const box = document.getElementById("fields");
  box.innerHTML = "";
  if (record.compute) {
    const banner = document.createElement("div");
    banner.className = "banner";
    banner.textContent = `Mode ${record.compute.mode}. Confirm required: ${record.needs_human_confirm}. Target: Snapdragon powered HP PC.`;
    box.appendChild(banner);
  }
  Object.entries(record).forEach(([key, value]) => {
    if (SKIP.has(key) || value === null || typeof value === "object") return;
    const row = document.createElement("div");
    row.className = "field-row";
    const label = document.createElement("label");
    label.textContent = key;
    const input = document.createElement("input");
    input.dataset.key = key;
    input.value = String(value);
    row.appendChild(label);
    row.appendChild(input);
    box.appendChild(row);
  });
  document.getElementById("letter").value = record.letter || "";
  document.getElementById("confirm-btn").disabled = false;
}

function collectEdits(record) {
  const next = { ...record };
  document.querySelectorAll("#fields input[data-key]").forEach((input) => {
    const key = input.dataset.key;
    const raw = input.value;
    const prev = record[key];
    next[key] = typeof prev === "number" && raw !== "" ? Number(raw) : raw;
  });
  return next;
}

document.getElementById("extract-form").addEventListener("submit", async (event) => {
  event.preventDefault();
  const status = document.getElementById("status");
  status.textContent = "Reading on this PC…";
  const data = new FormData();
  data.append("schema_name", document.getElementById("schema_name").value);
  data.append("language", document.getElementById("language").value);
  const image = document.getElementById("image").files[0];
  const audio = document.getElementById("audio").files[0];
  if (image) data.append("image", image);
  if (audio) data.append("audio", audio);
  try {
    const response = await fetch("/api/extract", { method: "POST", body: data });
    const payload = await response.json();
    if (!response.ok) throw new Error(payload.detail || "Extract failed");
    current = payload;
    renderFields(payload);
    status.textContent = payload.needs_human_confirm
      ? "Low confidence. Edit fields, then confirm."
      : "Ready to confirm.";
  } catch (error) {
    status.textContent = String(error.message || error);
  }
});

document.getElementById("confirm-btn").addEventListener("click", async () => {
  if (!current) return;
  const edited = collectEdits(current);
  const schemaName = document.getElementById("schema_name").value;
  const status = document.getElementById("export-status");
  status.textContent = "Writing local Excel…";
  try {
    const response = await fetch("/api/confirm", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ schema_name: schemaName, record: edited }),
    });
    const payload = await response.json();
    if (!response.ok) throw new Error(payload.detail || "Confirm failed");
    current = payload;
    status.innerHTML = `Saved record ${payload.record_id}. <a href="/api/export/${payload.record_id}">Download Excel</a>`;
  } catch (error) {
    status.textContent = String(error.message || error);
  }
});
