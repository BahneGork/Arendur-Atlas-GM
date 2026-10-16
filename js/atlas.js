/* Campaign atlas – map, pins, panel, search and the session-by-session journey. */
(async function () {
  const V = `?v=${window.ATLAS_VERSION || ""}`; // changes on every build, so phones fetch fresh files
  const data = await fetch(`data/atlas.json${V}`).then((r) => r.json());
  const { campaign, maps, places, regions, sessions, portals, offmap, unplaced, people, factions, threads, tools } = data;

  const UNIT = campaign.unit || "Session"; // what one step of Rejsen is called
  const KIND = {
    by: "By", borg: "Borg", taarn: "Tårn", hule: "Hule & dybde", helligt: "Helligt sted",
    havn: "Havn", vildmark: "Vildmark", sted: "Sted",
  };
  // 16x16 glyphs drawn inside the seal.
  const GLYPH = {
    by: "M3 8.5 8 4l5 4.5V13H9.5v-3h-3v3H3z",
    borg: "M3 13V5h2v1.6h1.6V5h2.8v1.6H11V5h2v8H9.6v-2.4H6.4V13z",
    taarn: "M6 13V6.2L8 3l2 3.2V13zM7.3 7.4h1.4v1.8H7.3z",
    hule: "M2 13c0-5.6 2.6-8.6 6-8.6s6 3 6 8.6h-3.4c0-2.6-1-4.4-2.6-4.4S5.4 10.4 5.4 13z",
    helligt: "M8 2.2l1.7 3.7 4 .4-3 2.7.9 4L8 11 4.4 13l.9-4-3-2.7 4-.4z",
    havn: "M7.3 5.6V11a3.3 3.3 0 0 1-2.7-1.9l1-.5-2.5-1L2.6 10l.9-.4A4.8 4.8 0 0 0 8 13a4.8 4.8 0 0 0 4.5-3.4l.9.4-.5-2.4-2.5 1 1 .5A3.3 3.3 0 0 1 8.7 11V5.6a1.6 1.6 0 1 0-1.4 0z",
    vildmark: "M1.8 13 6 5.4l2 3.4L10.2 5l4 8z",
    sted: "M8 4.5a3.5 3.5 0 1 1 0 7 3.5 3.5 0 0 1 0-7z",
  };

  const $ = (sel, el = document) => el.querySelector(sel);
  const el = (tag, attrs = {}, ...kids) => {
    const n = document.createElement(tag);
    for (const [k, v] of Object.entries(attrs)) {
      if (k === "class") n.className = v;
      else if (k.startsWith("on")) n.addEventListener(k.slice(2), v);
      else if (v !== false && v != null) n.setAttribute(k, v === true ? "" : v);
    }
    n.append(...kids.flat().filter((k) => k != null && k !== false));
    return n;
  };
  const fold = (s) => s.toLowerCase().replace(/æ/g, "ae").replace(/ø/g, "o").replace(/å/g, "a").normalize("NFKD").replace(/[\u0300-\u036f]/g, "");

  // ---------- Geometry helpers ----------
  const ll = ([x, y]) => L.latLng(-y, x);
  const children = (id) => Object.keys(places).filter((k) => places[k].parent === id);
  // Travel connections (teleportation circles and the like) at a place or inside it.
  const travelAt = (id) => [...(places[id].travel ? [id] : []), ...children(id).flatMap(travelAt)];
  const hasTravel = (id) => travelAt(id).length > 0;
  // Lost: the group no longer knows any of the ways at this pin.
  const travelLost = (id) => travelAt(id).every((k) => places[k].travelLost);
  // Where a place is drawn: its own pin, or the nearest ancestor with one.
  function anchor(id) {
    for (let cur = id; cur; cur = places[cur].parent) if (places[cur].at) return cur;
    return null;
  }
  function mapOf(id) {
    const a = anchor(id);
    if (a) return places[a].map;
    let cur = id;
    while (places[cur].parent) cur = places[cur].parent;
    const p = places[cur];
    if (p.region && regions[p.region]) return regions[p.region].map;
    if (p.offmap && offmap[p.offmap].map) return offmap[p.offmap].map;
    return null;
  }

  // ---------- Map ----------
  const map = L.map("map", {
    crs: L.CRS.Simple, zoomSnap: 0.25, zoomDelta: 0.5, minZoom: -4, maxZoom: 1.5,
    attributionControl: false, zoomControl: false, maxBoundsViscosity: 0.8,
  });
  L.control.zoom({ position: "bottomright" }).addTo(map);

  const layers = {};
  for (const [id, m] of Object.entries(maps)) {
    const [w, h] = m.size;
    const bounds = L.latLngBounds([[-h, 0], [0, w]]);
    layers[id] = {
      bounds,
      image: L.imageOverlay(m.image, bounds),
      regions: L.layerGroup(),
      pins: L.layerGroup(),
      trail: L.layerGroup(),
      influence: L.layerGroup(),
    };
  }

  const markers = {};
  function seal(id, approx = places[id].approx) {
    const p = places[id];
    const cls = ["pin", p.visited && "visited", approx && "approx", hasTravel(id) && "travel", hasTravel(id) && travelLost(id) && "travel-lost"].filter(Boolean).join(" ");
    return L.divIcon({
      className: cls, iconSize: [30, 38], iconAnchor: [15, 38],
      html: `<div class="pin-seal" role="img" aria-label="${p.name}"><svg viewBox="0 0 30 38" aria-hidden="true">
        <path class="body" d="M15 37C15 37 2 22.5 2 14.2A13 13 0 0 1 28 14.2C28 22.5 15 37 15 37Z"/>
        <g transform="translate(7 6)"><path class="glyph" d="${GLYPH[p.kind] || GLYPH.sted}"/></g>
        ${hasTravel(id) ? '<circle class="travel-ring" cx="25.5" cy="5" r="4.2"/>' : ""}</svg></div>`,
    });
  }
  // A place that stands for a whole other map (scroll=True) is drawn as a scroll and opens that map.
  const mapFor = (id) => Object.keys(maps).find((k) => maps[k].place === id);
  const scrollIcon = (id) => L.divIcon({
    className: "map-scroll", iconSize: [0, 0],
    html: `<span><b>${places[id].name}</b><small>Åbn kortet</small></span>`,
  });
  function addMarker(id) {
    const p = places[id];
    const scroll = p.scroll && mapFor(id);
    const m = L.marker(ll(p.at), { icon: scroll ? scrollIcon(id) : seal(id), keyboard: true, riseOnHover: true, title: scroll ? `Åbn kortet over ${p.name}` : "" });
    if (!scroll) m.bindTooltip(p.name, { className: "pin-label", direction: "top", offset: [0, -38] });
    m.on("click", () => go(scroll ? `kort/${scroll}` : `sted/${id}`));
    m.on("dragend", () => moved(id, m.getLatLng()));
    m.addTo(layers[p.map].pins);
    markers[id] = m;
  }
  for (const [id, p] of Object.entries(places)) if (p.at) addMarker(id);
  // The same place shown on further maps (e.g. a town on both the region map and the country map).
  // Their edits are keyed "<place>@<map>".
  const extraMarkers = [];
  const extraByKey = {};
  for (const [id, p] of Object.entries(places)) {
    for (const x of p.also || []) {
      const m = L.marker(ll(x.at), { icon: seal(id, x.approx), keyboard: true, riseOnHover: true });
      m.bindTooltip(p.name, { className: "pin-label", direction: "top", offset: [0, -38] });
      m.on("click", () => go(`sted/${id}`));
      m.on("dragend", () => movedExtra(`${id}@${x.map}`, m.getLatLng()));
      m.addTo(layers[x.map].pins);
      extraMarkers.push([id, m]);
      extraByKey[`${id}@${x.map}`] = { x, m, at: x.at };
    }
  }
  const regionLayers = {};
  for (const [id, r] of Object.entries(regions)) {
    if (!r.poly) continue;
    regionLayers[id] = L.polygon(r.poly.map(ll), { className: "region", interactive: true, smoothFactor: 1.5 })
      .on("click", (e) => { L.DomEvent.stop(e); go(`region/${id}`); })
      .addTo(layers[r.map].regions);
  }
  const signpost = (at, label, hint, route) =>
    L.marker(ll(at), {
      keyboard: true, title: label,
      icon: L.divIcon({ className: "signpost", iconSize: [0, 0], html: `<span>${label}<small>${hint}</small></span>` }),
    }).on("click", () => go(route));
  for (const p of portals) signpost(p.at, `${p.arrow || (p.to === campaign.start ? "↓" : "↑")} ${p.label}`, p.hint, `kort/${p.to}`).addTo(layers[p.map].pins);
  for (const [id, o] of Object.entries(offmap)) {
    if (o.map) signpost(o.at, `${o.name} →`, o.hint, `udenfor/${id}`).addTo(layers[o.map].pins);
  }

  // Marker elements are recreated when a map is re-added, so their state lives here.
  const pinState = { selected: null, here: null, seen: null, lit: null, onlyVisited: false, onlyTravel: false, editing: false };
  function applyPinState() {
    for (const [id, m] of Object.entries(markers)) {
      const e = m.getElement();
      if (!e) continue;
      e.classList.toggle("selected", id === pinState.selected);
      e.classList.toggle("current", !!pinState.here?.has(id));
      e.classList.toggle("dim", (!!pinState.seen && !pinState.seen.has(id)) || (!!pinState.lit && !pinState.lit.has(id)));
      e.classList.toggle("hidden", (pinState.onlyVisited && !places[id].visited) || (pinState.onlyTravel && !hasTravel(id)));
      e.classList.toggle("moved", !!edits[id]);
      m.options.draggable = pinState.editing;
      if (m.dragging) pinState.editing ? m.dragging.enable() : m.dragging.disable();
    }
    for (const [id, m] of extraMarkers) {
      const e = m.getElement();
      if (!e) continue;
      e.classList.toggle("selected", id === pinState.selected);
      e.classList.toggle("current", !!pinState.here?.has(id));
      e.classList.toggle("dim", (!!pinState.seen && !pinState.seen.has(id)) || (!!pinState.lit && !pinState.lit.has(id)));
      e.classList.toggle("hidden", (pinState.onlyVisited && !places[id].visited) || (pinState.onlyTravel && !hasTravel(id)));
    }
    for (const [key, { m }] of Object.entries(extraByKey)) {
      m.getElement()?.classList.toggle("moved", !!edits[key]);
      m.options.draggable = pinState.editing;
      if (m.dragging) pinState.editing ? m.dragging.enable() : m.dragging.disable();
    }
  }

  // ---------- Map switching ----------
  let current = null;
  const tabs = $(".map-tabs");
  for (const [id, m] of Object.entries(maps)) {
    tabs.append(el("button", { type: "button", "data-map": id, onclick: () => go(`kort/${id}`) }, m.name));
  }
  tabs.append(el("button", { type: "button", "data-map": "", onclick: () => go("udenfor/other") }, "Andre steder"));
  // Features without data yet are left out rather than shown empty.
  if (Object.keys(people).length) tabs.append(el("button", { type: "button", "data-map": "personer", onclick: () => go("personer") }, "Personer"));
  if (threads.length) tabs.append(el("button", { type: "button", "data-map": "traade", onclick: () => go("traade") }, "Tråde"));

  function showMap(id, fit = true) {
    if (current !== id) {
      if (current) for (const k of ["image", "regions", "pins", "trail", "influence"]) map.removeLayer(layers[current][k]);
      current = id;
      const lyr = layers[id];
      for (const k of ["image", "regions", "pins", "trail", "influence"]) lyr[k].addTo(map);
      // Fit before setting limits, so the limits never trigger their own (animated) zoom.
      map.setMaxBounds(null);
      map.options.minZoom = -4;
      map.fitBounds(lyr.bounds, { animate: false });
      map.setMinZoom(map.getZoom() - 0.5);
      map.setMaxBounds(lyr.bounds.pad(0.25));
      fit = false;
    }
    for (const b of tabs.children) b.setAttribute("aria-pressed", String(b.dataset.map === id));
    if (fit) map.fitBounds(layers[id].bounds, { animate: false });
    applyPinState();
  }

  // flyToBounds ignores maxBounds, so the map flies past the edge and then snaps back.
  // Clamp the destination first so every move is a single smooth flight.
  function flyWithin(bounds, opts) {
    const { center, zoom } = map._getBoundsCenterZoom(bounds, opts);
    map.flyTo(map._limitCenter(center, zoom, map.options.maxBounds), zoom, { duration: opts.duration });
  }

  function focusPin(id) {
    const a = anchor(id);
    // Stay on the current map when the place has a pin here too.
    const here = a && (places[a].also || []).find((x) => x.map === current);
    if (here) {
      const pt = ll(here.at);
      flyWithin(L.latLngBounds(pt, pt), { maxZoom: Math.max(map.getZoom(), -0.75), duration: 0.6, paddingBottomRight: panelPadding() });
      return;
    }
    const target = mapOf(id);
    if (target) showMap(target, false);
    if (a) {
      const pt = ll(places[a].at);
      flyWithin(L.latLngBounds(pt, pt), {
        maxZoom: Math.max(map.getZoom(), -0.75), duration: 0.6, paddingBottomRight: panelPadding(),
      });
    } else if (target) map.fitBounds(layers[target].bounds);
  }

  // Space taken by the open side panel (right on desktop, bottom sheet on phones).
  function panelPadding() {
    if (window.innerWidth <= 720) return [0, Math.round(window.innerHeight * 0.62)];
    return [424, 0];
  }

  function select(id) {
    pinState.selected = id;
    applyPinState();
  }

  // ---------- Panel ----------
  const panel = $(".panel");
  const body = $(".panel-body");
  // Closing the panel keeps Rejsen open if it is.
  const closeRoute = () => (jBody.hidden ? "" : `session/${sessions[step].num}`);
  $(".panel-close").addEventListener("click", () => go(closeRoute()));

  function openPanel(...content) {
    body.replaceChildren(...content.flat(2).filter(Boolean));
    panel.classList.remove("wide");
    panel.hidden = false;
    body.scrollTop = 0;
  }
  function closePanel() {
    panel.hidden = true;
    select(null);
    clearInfluence();
    markSessions([]);
    for (const r of Object.values(regionLayers)) r.getElement()?.classList.remove("selected");
  }

  const placeButton = (id) => {
    const p = places[id];
    return el("li", {}, el("button", { type: "button", onclick: () => go(`sted/${id}`) },
      el("span", { class: `dot${p.visited ? " visited" : ""}` }), p.name, p.approx ? el("small", {}, "omtrentlig") : null));
  };
  function placeList(title, ids, limit = 12) {
    if (!ids.length) return null;
    ids = [...ids].sort((a, b) => (places[b].visited - places[a].visited) || places[a].name.localeCompare(places[b].name, "da"));
    const list = el("ul", { class: "places-list" }, ids.slice(0, limit).map(placeButton));
    const more = ids.length > limit
      ? el("button", { type: "button", class: "more", onclick: (e) => { list.append(...ids.slice(limit).map(placeButton)); e.target.remove(); } },
          `Vis alle ${ids.length}`)
      : null;
    return [el("h3", {}, title), list, more];
  }
  // entries are [name, noteId]; names with a note open it in the reader
  function chips(title, entries, limit = 14) {
    if (!entries.length) return null;
    const chip = ([name, id]) => el("li", {}, id ? el("a", { href: `#note/${id}` }, name) : name);
    const list = el("ul", { class: "chips" }, entries.slice(0, limit).map(chip));
    const more = entries.length > limit
      ? el("button", { type: "button", class: "more", onclick: (e) => { list.append(...entries.slice(limit).map(chip)); e.target.remove(); } },
          `+ ${entries.length - limit} mere`)
      : null;
    return [el("h3", {}, title), list, more];
  }
  const noteLink = (noteId, url) => el("div", { class: "note-actions" },
    noteId ? el("a", { class: "note-link", href: `#note/${noteId}` }, "Læs hele noten →") : null,
    url ? el("a", { class: "garden-link", href: url, target: "_blank", rel: "noopener" }, "Åbn i haven ↗") : null);

  // Summaries carry [name](#note/<id>) links to the notes they mention.
  function summary(md) {
    const p = el("p", { class: "summary" });
    p.innerHTML = marked.parseInline(md);
    return p;
  }

  function crumbs(id) {
    const trail = [];
    let cur = places[id].parent;
    while (cur) { trail.unshift(["sted/" + cur, places[cur].name]); cur = places[cur].parent; }
    let top = id;
    while (places[top].parent) top = places[top].parent;
    const p = places[top];
    if (p.region && regions[p.region]) trail.unshift([`region/${p.region}`, regions[p.region].name]);
    const m = mapOf(id);
    if (m) trail.unshift([`kort/${m}`, maps[m].name]);
    if (p.offmap) trail.unshift([`udenfor/${p.offmap}`, offmap[p.offmap].name]);
    return el("p", { class: "crumbs" }, trail.flatMap(([route, name], i) => [
      i ? " › " : null, el("button", { type: "button", onclick: () => go(route) }, name)]));
  }

  // ---------- People ----------
  const STANCE = { ally: "Allieret", neutral: "Neutral", enemy: "Fjende", unknown: "Ukendt" };
  const STATUS = { active: "aktiv", weakened: "svækket", defunct: "opløst", missing: "savnet", undead: "udød",
    captured: "fanget", unknown: "ukendt" };
  const statusText = (s) => STATUS[s] || s;
  // A person's place is a place id, or "region:<id>".
  const placeName = (ref) => (!ref ? "Ukendt opholdssted"
    : ref.startsWith("region:") ? regions[ref.slice(7)]?.name : places[ref]?.name) || "Ukendt opholdssted";
  const placeRoute = (ref) => (ref?.startsWith("region:") ? `region/${ref.slice(7)}` : `sted/${ref}`);
  const initials = (name) => name.replace(/\(.*?\)/g, "").split(/[\s-]+/).filter((w) => /^[A-ZÆØÅ]/i.test(w))
    .slice(0, 2).map((w) => w[0].toUpperCase()).join("");
  const monogram = (pid, big = false) => {
    const p = people[pid];
    return el("span", { class: `monogram stance-${p.stance}${p.dead ? " dead" : ""}${p.pc ? " pc" : ""}${big ? " big" : ""}`, "aria-hidden": "true" },
      initials(p.name), p.dead ? el("i", {}, "†") : null);
  };
  const personMeta = (p, withPlace) => [p.social, p.role, withPlace ? (p.pc ? "med gruppen" : placeName(p.place)) : null]
    .filter(Boolean).filter((v, i, a) => a.indexOf(v) === i).join(" · ");
  const personRow = (pid, withPlace = false) => {
    const p = people[pid];
    return el("li", {}, el("a", { class: "person-row", href: `#note/${pid}` },
      monogram(pid), el("span", {}, el("b", {}, p.name, p.dead ? " †" : ""), el("small", {}, personMeta(p, withPlace)))));
  };
  const byName = (a, b) => people[a].name.localeCompare(people[b].name, "da");
  // Session chips; the party is in most sessions, so they get a summary with the list folded away.
  function sessionChips(p) {
    const list = el("div", { class: "chips" }, p.sessions.map((num) =>
      el("a", { class: "session-link", href: `#session/${num}/laes` }, `${UNIT} ${num}`)));
    if (!p.pc || p.sessions.length <= 8) return list;
    const [first, last] = p.period || [p.sessions[0], p.sessions[p.sessions.length - 1]];
    const link = (n) => el("a", { class: "session-link", href: `#session/${n}/laes` }, `S${n}`);
    return el("details", { class: "session-summary" },
      el("summary", {}, "Med i gruppen fra ", link(first), last != null ? [" til ", link(last)] : " og frem",
        ` · ${p.sessions.length} sessioner`),
      list);
  }
  // All places inside a place (Soltræet and its chambers are inside Astley, …).
  const subtree = (id) => [id, ...children(id).flatMap(subtree)];

  // ---------- Factions ----------
  const FTYPE = { tribe: "stamme", "knightly-order": "ridderorden", clan: "klan", "noble-house": "adelshus",
    "religious-order": "religiøs orden", "political-body": "politisk organ", "arcane-order": "arkan orden",
    court: "hof", guild: "laug", family: "familie", organization: "organisation", military: "militær",
    cult: "kult", "merchant-guild": "købmandslaug" };
  const ftype = (t) => t.split(/,\s*/).map((x) => FTYPE[x] || x.replace(/-/g, " ")).join(", ");
  const banner = (fid, big = false) => el("span", { class: `banner stance-${factions[fid].stance}${big ? " big" : ""}`, "aria-hidden": "true" });
  const byFaction = (a, b) => factions[a].name.localeCompare(factions[b].name, "da");
  const factionRow = (fid) => {
    const f = factions[fid];
    return el("li", {}, el("a", { class: "person-row", href: `#note/${fid}` }, banner(fid),
      el("span", {}, el("b", {}, f.name),
        el("small", {}, [ftype(f.type), f.seat ? placeName(f.seat) : null].filter(Boolean).join(" · ")))));
  };
  function factionSection(ids) {
    ids = [...new Set(ids)].filter((k) => factions[k]).sort(byFaction);
    if (!ids.length) return null;
    const list = el("ul", { class: "people-list" }, ids.slice(0, 10).map(factionRow));
    const more = ids.length > 10
      ? el("button", { type: "button", class: "more", onclick: (e) => { list.append(...ids.slice(10).map(factionRow)); e.target.remove(); } },
          `Vis alle ${ids.length}`)
      : null;
    return [el("h3", {}, `Factions (${ids.length})`), list, more];
  }
  // Factions present at a set of place refs: seated there, members living there, or named in the place's note.
  const factionsAt = (refs, linked) => Object.keys(factions).filter((fid) => refs.includes(factions[fid].seat)
    || factions[fid].members.some((pid) => refs.includes(people[pid]?.place))).concat(linked);

  // Sphere of influence: the seat, where members live and places that name the faction, joined by ink lines.
  function clearInfluence() {
    for (const lyr of Object.values(layers)) lyr.influence.clearLayers();
    if (pinState.lit) { pinState.lit = null; applyPinState(); }
  }
  function showInfluence(fid) {
    stopPlay(); endJourney();
    clearInfluence();
    const f = factions[fid];
    const refs = [f.seat, ...f.members.map((pid) => people[pid]?.place),
      ...Object.keys(places).filter((k) => places[k].factions.some(([, id]) => id === fid))].filter(Boolean);
    const pins = [...new Set(refs.filter((r) => !r.startsWith("region:")).map(anchor).filter(Boolean))];
    if (!pins.length) return false;
    const seat = f.seat && !f.seat.startsWith("region:") ? anchor(f.seat) : null;
    const target = seat ? places[seat].map
      : Object.keys(maps).sort((a, b) => pins.filter((k) => places[k].map === b).length - pins.filter((k) => places[k].map === a).length)[0];
    showMap(target, false);
    const here = pins.filter((k) => places[k].map === target);
    if (seat) for (const k of here) if (k !== seat)
      L.polyline([ll(places[seat].at), ll(places[k].at)], { className: "influence-line", interactive: false }).addTo(layers[target].influence);
    pinState.lit = new Set(pins);
    select(seat);
    flyWithin(L.latLngBounds(here.map((k) => ll(places[k].at))), { maxZoom: -0.5, duration: 0.8,
      paddingTopLeft: [120, 120], paddingBottomRight: window.innerWidth > 720 ? [660, 120] : [40, Math.round(window.innerHeight * 0.62)] });
    return true;
  }

  // People list for a place/region panel: residents first, then people whose notes mention it.
  function peopleSection(residents, mentioned) {
    const ids = [...new Set([...residents.sort(byName), ...mentioned.filter((k) => people[k]).sort(byName)])];
    if (!ids.length) return null;
    const list = el("ul", { class: "people-list" }, ids.slice(0, 12).map((k) => personRow(k)));
    const more = ids.length > 12
      ? el("button", { type: "button", class: "more", onclick: (e) => { list.append(...ids.slice(12).map((k) => personRow(k))); e.target.remove(); } },
          `Vis alle ${ids.length}`)
      : null;
    return [el("h3", {}, `Personer (${ids.length})`), list, more];
  }

  // Directory (#personer or #personer/<filter>): the way to look for someone.
  // Properties are mostly English; add the Danish word so "dværg", "præst", "købmand" … also match.
  const DANISH = { dwarf: "dværg", gnome: "gnom", elf: "elver", human: "menneske", halfling: "halvling",
    kobold: "kobold", dragonborn: "dragefødt", orc: "ork", giant: "kæmpe", priest: "præst", cleric: "præst",
    merchant: "købmand", knight: "ridder", commoner: "almindelig borger", royalty: "kongelig", noble: "adelig",
    officer: "officer", guard: "vagt", soldier: "soldat", innkeeper: "kro krovært", wizard: "troldmand",
    mage: "troldmand magiker", druid: "druide", scholar: "lærd", thief: "tyv", smith: "smed", blacksmith: "smed",
    farmer: "bonde", sailor: "sømand", captain: "kaptajn", hunter: "jæger", healer: "healer helbreder" };
  const danish = (text) => text.toLowerCase().split(/[^a-z]+/).map((w) => DANISH[w] || "").join(" ");
  const personKeys = Object.fromEntries(Object.entries(people).map(([pid, p]) => [pid, fold([
    p.name, ...p.aliases, p.role, p.social, p.race, danish(`${p.role} ${p.social} ${p.race}`), p.pc ? "gruppen spillerkarakter" : "",
    placeName(p.place), ...p.factions.map((f) => factions[f]?.name || ""),
  ].join(" "))]));
  const DIR_FILTERS = [["pc", "Gruppen"], ["ally", "Allierede"], ["neutral", "Neutrale"], ["enemy", "Fjender"], ["unknown", "Ukendte"], ["dead", "Døde"]];
  const dirState = { q: "", only: null };
  function showDirectory(q = "") {
    dirState.q = q;
    for (const b of tabs.children) b.setAttribute("aria-pressed", String(b.dataset.map === "personer"));
    const field = el("input", { type: "search", class: "dir-filter", placeholder: "Navn, rolle, sted, faction…", value: q,
      "aria-label": "Filtrér personer" });
    const chipsRow = el("div", { class: "dir-chips" });
    const out = el("div", { class: "dir-results" });
    const matches = (pid) => {
      const p = people[pid];
      const words = fold(dirState.q).split(/\s+/).filter(Boolean);
      return words.every((w) => personKeys[pid].includes(w))
        && (!dirState.only || (dirState.only === "dead" ? p.dead : dirState.only === "pc" ? p.pc : p.stance === dirState.only));
    };
    function render() {
      const textHits = Object.keys(people).filter((pid) => fold(dirState.q).split(/\s+/).filter(Boolean).every((w) => personKeys[pid].includes(w)));
      chipsRow.replaceChildren(...DIR_FILTERS.map(([key, label]) => {
        const n = textHits.filter((pid) => (key === "dead" ? people[pid].dead : key === "pc" ? people[pid].pc : people[pid].stance === key)).length;
        return el("button", { type: "button", class: `dir-chip stance-${key}`, "aria-pressed": String(dirState.only === key),
          onclick: () => { dirState.only = dirState.only === key ? null : key; render(); } }, `${label} ${n}`);
      }));
      const hits = Object.keys(people).filter(matches);
      const groups = {};
      for (const pid of hits) (groups[people[pid].pc ? "party" : people[pid].place || ""] ||= []).push(pid);
      const order = Object.keys(groups).sort((a, b) => (b === "party") - (a === "party")
        || (a === "") - (b === "") || groups[b].length - groups[a].length);
      out.replaceChildren(
        el("p", { class: "dir-count" }, `${hits.length} af ${Object.keys(people).length} personer`),
        ...order.map((ref) => {
          const ids = groups[ref].sort(byName);
          const limit = ref === "party" ? Infinity : 8; // the party is always shown in full
          const list = el("ul", { class: "people-list" }, ids.slice(0, limit).map((k) => personRow(k)));
          return el("section", { class: "dir-group" },
            el("h3", {}, ref === "party" ? "Med gruppen" : ref ? el("a", { href: `#${placeRoute(ref)}` }, placeName(ref)) : "Ukendt opholdssted", ` (${ids.length})`),
            list,
            ids.length > limit ? el("button", { type: "button", class: "more",
              onclick: (e) => { list.append(...ids.slice(limit).map((k) => personRow(k))); e.target.remove(); } }, `Vis alle ${ids.length}`) : null);
        }));
    }
    field.addEventListener("input", () => {
      dirState.q = field.value;
      history.replaceState(null, "", `#personer${field.value ? "/" + encodeURIComponent(field.value) : ""}`);
      render();
    });
    render();
    openPanel(el("p", { class: "kicker" }, "Personregister"), el("h2", {}, "Personer"), field, chipsRow, out);
    if (window.innerWidth > 720) field.focus();
  }

  function showPlace(id) {
    const p = places[id];
    const kids = children(id);
    // Everything that happened inside this place counts towards its sessions.
    const sess = new Set(p.sessions);
    const walk = (k) => { places[k].sessions.forEach((s) => sess.add(s)); children(k).forEach(walk); };
    kids.forEach(walk);
    openPanel(
      crumbs(id),
      el("p", { class: "kicker" }, KIND[p.kind] || "Sted"),
      el("h2", {}, p.name),
      el("div", { class: "badges" },
        p.visited ? el("span", { class: "badge visited" }, "Besøgt") : el("span", { class: "badge" }, "Kun hørt om"),
        p.approx ? el("span", { class: "badge approx" }, "Omtrentlig placering") : null,
        p.travel ? el("span", { class: `badge travel${p.travelLost ? " lost" : ""}` }, p.travelLost ? "Rejsemulighed – glemt" : "Rejsemulighed") : null,
        !p.at && !anchor(id) ? el("span", { class: "badge approx" }, "Ikke på kortet") : null),
      p.summary ? summary(p.summary) : null,
      p.where ? el("p", { class: "where" }, p.where) : null,
      p.gm ? el("div", { class: "gm-note" }, el("strong", {}, "Kun GM"), summary(p.gm)) : null,
      p.travel ? el("p", { class: "travel-note" }, p.travel) : null,
      Object.entries(maps).filter(([, m]) => m.place === id).map(([mid, m]) =>
        el("p", {}, el("button", { type: "button", class: "session-chip", onclick: () => go(`kort/${mid}`) }, `Åbn kortet over ${m.name} →`))),
      sess.size ? [el("h3", {}, "Her har vi været"),
        el("div", { class: "chips" }, [...sess].sort((a, b) => a - b).map((n) =>
          el("button", { type: "button", class: "session-chip", title: sessionByNum(n)?.title, onclick: () => go(`session/${n}`) }, `${UNIT} ${n}`)))] : null,
      placeList("Steder her", kids),
      peopleSection(Object.keys(people).filter((k) => subtree(id).includes(people[k].place)),
        subtree(id).flatMap((k) => places[k].people.map(([, pid]) => pid))),
      factionSection(factionsAt(subtree(id), subtree(id).flatMap((k) => places[k].factions.map(([, fid]) => fid)))),
      noteLink(p.noteId, p.url),
    );
    focusPin(id);
    select(anchor(id));
  }

  function showRegion(id) {
    const r = regions[id];
    const members = Object.keys(places).filter((k) => places[k].region === id && !places[k].parent);
    showMap(r.map, false);
    openPanel(
      el("p", { class: "crumbs" }, el("button", { type: "button", onclick: () => go(`kort/${r.map}`) }, maps[r.map].name)),
      el("p", { class: "kicker" }, r.poly ? "Baroni" : "Land"),
      el("h2", {}, r.name),
      r.summary ? summary(r.summary) : null,
      placeList(r.poly ? "Steder i baroniet" : "Steder uden kendt placering", members),
      peopleSection(Object.keys(people).filter((k) => people[k].place === `region:${id}`
        || (places[people[k].place] && places[anchor(people[k].place) || people[k].place]?.region === id)),
        r.people.map(([, pid]) => pid)),
      factionSection(factionsAt([`region:${id}`, ...Object.keys(places).filter((k) => places[k].region === id).flatMap(subtree)],
        r.factions.map(([, fid]) => fid))),
      noteLink(r.noteId, r.url),
    );
    select(null);
    for (const [k, l] of Object.entries(regionLayers)) l.getElement()?.classList.toggle("selected", k === id);
    if (r.poly) flyWithin(L.latLngBounds(r.poly.map(ll)), { duration: 0.6, paddingTopLeft: [40, 40], paddingBottomRight: panelPadding() });
  }

  function showMapPanel(id) {
    const regionId = Object.keys(regions).find((k) => regions[k].map === id && !regions[k].poly);
    showMap(id, true);
    if (regionId) showRegion(regionId);
    else closePanel();
  }

  function showOffmap(id) {
    const o = offmap[id];
    if (o.map) showMap(o.map, false);
    for (const b of tabs.children) b.setAttribute("aria-pressed", String(!o.map && b.dataset.map === ""));
    openPanel(
      el("p", { class: "kicker" }, "Uden for kortene"),
      el("h2", {}, o.name),
      el("p", { class: "summary" }, o.summary || "Steder fra noterne, hvor vi ikke kender placeringen – eller som slet ikke ligger i denne verden."),
      placeList("Steder", Object.keys(places).filter((k) => places[k].offmap === id), 30),
    );
  }

  // ---------- Search ----------
  // On phones the search field sits just below the title panel, whose height depends on how the tabs wrap.
  function placeSearch() {
    const search = $(".search");
    search.style.top = window.innerWidth <= 720 ? `${Math.round($(".cartouche").getBoundingClientRect().bottom + 8)}px` : "";
  }
  window.addEventListener("resize", placeSearch);
  document.fonts?.ready.then(placeSearch);
  placeSearch();

  const input = $("#search-input");
  const results = $(".search-results");
  const index = [
    ...Object.entries(places).map(([id, p]) => ({ route: `sted/${id}`, name: p.name, sub: KIND[p.kind], keys: [p.name, ...p.aliases].map(fold) })),
    ...Object.entries(regions).map(([id, r]) => ({ route: `region/${id}`, name: r.name, sub: r.poly ? "Baroni" : "Land", keys: [fold(r.name)] })),
    ...Object.entries(people).map(([id, p]) => ({ route: `note/${id}`, name: p.name + (p.dead ? " †" : ""),
      sub: p.pc ? "Gruppen" : `Person${p.place ? " · " + placeName(p.place) : ""}`, keys: [p.name, ...p.aliases].map(fold) })),
    ...Object.entries(factions).map(([id, f]) => ({ route: `note/${id}`, name: f.name, sub: "Faction", keys: [fold(f.name)] })),
  ];
  let active = 0;
  function renderResults() {
    const q = fold(input.value.trim());
    if (!q) { results.hidden = true; return; }
    const hits = index
      .map((e) => ({ e, score: Math.min(...e.keys.map((k) => (k.startsWith(q) ? 0 : k.includes(q) ? 1 : 9))) }))
      .filter((h) => h.score < 9).sort((a, b) => a.score - b.score || a.e.name.localeCompare(b.e.name, "da")).slice(0, 10);
    active = 0;
    results.replaceChildren(...(hits.length ? hits.map(({ e }, i) => el("li", {
      role: "option", "aria-selected": String(i === 0), onmousedown: (ev) => { ev.preventDefault(); pick(e); },
    }, e.name, el("small", {}, e.sub))) : [el("li", {}, "Ingen steder fundet")]));
    results.hits = hits.map((h) => h.e);
    results.hidden = false;
  }
  function pick(e) { input.value = ""; results.hidden = true; input.blur(); go(e.route); }
  input.addEventListener("input", renderResults);
  input.addEventListener("blur", () => { results.hidden = true; });
  input.addEventListener("keydown", (ev) => {
    const hits = results.hits || [];
    if (ev.key === "ArrowDown" || ev.key === "ArrowUp") {
      ev.preventDefault();
      active = (active + (ev.key === "ArrowDown" ? 1 : -1) + hits.length) % Math.max(hits.length, 1);
      [...results.children].forEach((li, i) => li.setAttribute("aria-selected", String(i === active)));
    } else if (ev.key === "Enter" && hits[active]) pick(hits[active]);
    else if (ev.key === "Escape") { input.value = ""; results.hidden = true; }
  });

  // ---------- Legend ----------
  const legendBody = $(".legend-body");
  $(".legend-toggle").addEventListener("click", (e) => {
    legendBody.hidden = !legendBody.hidden;
    e.currentTarget.setAttribute("aria-expanded", String(!legendBody.hidden));
  });
  $("#opt-regions").addEventListener("change", (e) => document.body.classList.toggle("regions-off", !e.target.checked));
  $("#opt-visited").addEventListener("change", (e) => {
    pinState.onlyVisited = e.target.checked;
    applyPinState();
  });
  $("#opt-travel").addEventListener("change", (e) => {
    pinState.onlyTravel = e.target.checked;
    applyPinState();
  });

  // ---------- Journey ----------
  const journey = $(".journey");
  const jBody = $(".journey-body");
  const jToggle = $(".journey-toggle");
  const strip = $(".journey-strip");
  const card = $(".journey-card");
  let step = -1; // index into sessions
  let timer = null;
  const sessionByNum = (num) => sessions.find((s) => String(s.num) === String(num));
  // Gold dots on the timeline for the sessions of the person/faction being read.
  function markSessions(nums) {
    const set = new Set(nums.map(String));
    [...strip.children].forEach((li, i) => li.firstChild.classList.toggle("featured", set.has(String(sessions[i].num))));
    // Bring the first dot into view without scrolling the page.
    const first = strip.querySelector(".featured");
    if (first && !jBody.hidden) strip.scrollTo({ left: first.offsetLeft - 40, behavior: "smooth" });
  }

  const sessionMap = (s) => s.places.map(mapOf).find(Boolean) || null;
  for (const s of sessions) {
    strip.append(el("li", {}, el("button", {
      type: "button", class: `gm-${s.gm.toLowerCase()}${sessionMap(s) ? "" : " offmap"}`,
      title: `${UNIT} ${s.num}: ${s.title}`, onclick: () => go(`session/${s.num}`),
    }, String(s.num))));
  }
  jToggle.addEventListener("click", () => {
    if (jBody.hidden) go(`session/${sessions[Math.max(step, 0)].num}`);
    else { stopPlay(); endJourney(); go(""); }
  });
  $(".journey-controls").addEventListener("click", (e) => {
    const b = e.target.closest("button");
    if (!b) return;
    if (b.classList.contains("journey-play")) return timer ? stopPlay() : startPlay();
    stopPlay();
    go(`session/${sessions[Math.min(sessions.length - 1, Math.max(0, step + Number(b.dataset.step)))].num}`);
  });
  function startPlay() {
    $(".journey-play").textContent = "❚❚";
    if (step >= sessions.length - 1) go(`session/${sessions[0].num}`);
    timer = setInterval(() => {
      if (step >= sessions.length - 1) return stopPlay();
      go(`session/${sessions[step + 1].num}`);
    }, 2600);
  }
  function stopPlay() {
    clearInterval(timer); timer = null;
    $(".journey-play").textContent = "▶";
  }

  function endJourney() {
    jBody.hidden = true;
    jToggle.setAttribute("aria-expanded", "false");
    for (const lyr of Object.values(layers)) lyr.trail.clearLayers();
    pinState.here = pinState.seen = null;
    applyPinState();
  }

  function showSession(idx, reading = false) {
    step = idx;
    const s = sessions[idx];
    jBody.hidden = false;
    jToggle.setAttribute("aria-expanded", "true");
    closePanel();
    [...strip.children].forEach((li, i) => {
      const b = li.firstChild;
      b.classList.toggle("past", i < idx);
      b.setAttribute("aria-current", String(i === idx));
      if (i === idx) b.scrollIntoView({ block: "nearest", inline: "center", behavior: "smooth" });
    });

    const target = sessionMap(s);
    const names = s.places.map((id) => places[id].name);
    card.replaceChildren(
      el("p", { class: "meta" }, `${UNIT} ${s.num}${s.date ? " · " + s.date : ""}${s.gm ? " · spilleder " + s.gm : ""}`),
      el("h2", {}, s.title),
      s.summary ? el("p", {}, s.summary) : null,
      el("p", {},
        names.length ? `${[...new Set(names)].join(", ")}. ` : "Uden for kortene. ",
        s.noteId ? el("a", { class: "read-session", href: `#session/${s.num}/laes` }, campaign.readLabel || "Læs sessionen og se relaterede noter") : null),
    );

    // Trail: every earlier stop on this map, in order; the current session's leg in wax.
    for (const lyr of Object.values(layers)) lyr.trail.clearLayers();
    const stops = [];
    for (const t of sessions.slice(0, idx + 1)) {
      for (const id of t.places) {
        const a = anchor(id);
        if (!a) continue;
        const last = stops[stops.length - 1];
        if (!last || last.id !== a) stops.push({ id: a, map: places[a].map, num: t.num });
      }
    }
    for (const mapId of Object.keys(maps)) {
      const pts = stops.filter((st) => st.map === mapId);
      for (let i = 1; i < pts.length; i++) {
        const now = pts[i].num === s.num;
        L.polyline([ll(places[pts[i - 1].id].at), ll(places[pts[i].id].at)], { className: `trail${now ? " now" : ""}`, interactive: false })
          .addTo(layers[mapId].trail);
      }
    }

    const here = new Set(s.places.map(anchor).filter(Boolean));
    pinState.here = here;
    pinState.seen = new Set(stops.map((st) => st.id));
    applyPinState();
    if (target) {
      showMap(target, false);
      const pts = [...here].filter((id) => places[id].map === target).map((id) => ll(places[id].at));
      // Only move when this session's places are not already comfortably in view (above the journey card);
      // re-centring on the same spot makes the small Nordheim map bounce against its edges.
      const card = jBody.getBoundingClientRect();
      const bottomPad = window.innerHeight - card.top + 40;
      // The reader panel takes the right-hand side on wide screens.
      const rightPad = reading && window.innerWidth > 720 ? 660 : 120;
      const inView = (pt) => {
        const px = map.latLngToContainerPoint(pt);
        const size = map.getSize();
        return px.x > 80 && px.x < size.x - rightPad + 40 && px.y > 80 && px.y < size.y - bottomPad;
      };
      if (pts.length && !pts.every(inView)) {
        flyWithin(L.latLngBounds(pts), { maxZoom: -0.5, duration: 0.8, paddingTopLeft: [120, 120], paddingBottomRight: [rightPad, bottomPad] });
      } else if (!pts.length) flyWithin(layers[target].bounds, { duration: 0.8 });
    }
  }

  // ---------- Edit mode: move pins, export the changes ----------
  // Changes live in this browser only; "Kopiér ændringer" hands them over for tools/apply_moves.py.
  const REPO = campaign.repo;
  // Per atlas: several atlases share the github.io origin and so the same localStorage.
  const EDITS_KEY = `atlas-edits:${REPO}`;
  const editbar = $(".editbar");
  const editStatus = $(".editbar-status");
  const editExport = $(".editbar-export");
  const unplacedList = $(".unplaced-list");
  const original = Object.fromEntries(Object.entries(places).map(([id, p]) => [id, { map: p.map, at: p.at, offmap: p.offmap }]));
  let edits = {};
  let placing = null;
  try { edits = JSON.parse(localStorage.getItem(EDITS_KEY)) || {}; } catch { edits = {}; }
  // Edits the published data already contains (saved for everyone) are done; drop them.
  for (const [id, e] of Object.entries(edits)) {
    const xa = extraByKey[id]?.x.at;
    if (xa && xa[0] === e.at?.[0] && xa[1] === e.at?.[1]) { delete edits[id]; continue; }
    const p = places[id];
    if (p && p.map === e.map && p.at?.[0] === e.at?.[0] && p.at?.[1] === e.at?.[1]) delete edits[id];
  }
  try { localStorage.setItem(EDITS_KEY, JSON.stringify(edits)); } catch { /* private mode */ }

  const xy = (latlng) => [Math.round(latlng.lng), Math.round(-latlng.lat)];
  function saveEdits() {
    try { localStorage.setItem(EDITS_KEY, JSON.stringify(edits)); } catch { /* private mode: keep in memory */ }
    const n = Object.keys(edits).length;
    editStatus.textContent = n ? `${n} ${n === 1 ? "ændring" : "ændringer"} gemt i denne browser.` : "Ingen ændringer endnu.";
    editExport.hidden = true;
  }
  function moved(id, latlng) {
    places[id].at = xy(latlng);
    edits[id] = { ...edits[id], map: places[id].map, at: places[id].at };
    saveEdits();
    applyPinState();
  }
  function movedExtra(key, latlng) {
    extraByKey[key].x.at = xy(latlng);
    edits[key] = { map: extraByKey[key].x.map, at: extraByKey[key].x.at };
    saveEdits();
    applyPinState();
  }
  // A location note that is not in the atlas yet becomes a plain place once it is put on the map.
  function newPlace(id, note) {
    places[id] = { name: note, note, kind: "sted", approx: true, visited: false, sessions: [], people: [],
                   factions: [], aliases: [], summary: unplaced.find((u) => u.note === note)?.summary || "",
                   url: unplaced.find((u) => u.note === note)?.url || "", where: "", isNew: true };
  }
  const slug = (s) => fold(s).replace(/[^a-z0-9]+/g, "-").replace(/^-|-$/g, "");
  function applyEdit(id, e) {
    if (extraByKey[id]) {
      extraByKey[id].x.at = e.at;
      extraByKey[id].m.setLatLng(ll(e.at));
      return;
    }
    if (id.includes("@")) return; // an extra pin that no longer exists
    if (!places[id] && e.note) newPlace(id, e.note);
    const p = places[id];
    if (!p || !layers[e.map]) return;
    p.map = e.map;
    p.at = e.at;
    if (markers[id]) {
      markers[id].setLatLng(ll(e.at));
      if (!layers[e.map].pins.hasLayer(markers[id])) {
        for (const lyr of Object.values(layers)) lyr.pins.removeLayer(markers[id]);
        markers[id].addTo(layers[e.map].pins);
      }
    } else addMarker(id);
  }
  // Places in the atlas without a position, plus location notes the atlas does not know yet.
  function fillPlaceSelect() {
    const known = Object.keys(places).filter((id) => !places[id].at && !places[id].parent)
      .map((id) => ({ id, name: places[id].name, hint: places[id].offmap ? offmap[places[id].offmap].name : "uden position" }));
    const fresh = unplaced.filter((u) => !places[slug(u.note)])
      .map((u) => ({ id: slug(u.note), note: u.note, name: u.note, hint: "ny note" }));
    const items = [...fresh, ...known].sort((a, b) => a.name.localeCompare(b.name, "da"));
    $(".unplaced-count").textContent = `(${items.length})`;
    unplacedList.replaceChildren(...items.map((it) => el("li", {},
      el("button", { type: "button", "aria-pressed": String(placing?.id === it.id), onclick: () => startPlacing(it) },
        it.name, el("small", {}, it.hint)))));
  }
  function startPlacing(it) {
    placing = it;
    $(".unplaced").open = false;
    editStatus.textContent = `Klik på kortet, hvor ${it.name} ligger. (Skift kort øverst til venstre, hvis det ligger på et andet kort.)`;
    fillPlaceSelect();
  }
  function setEditing(on) {
    pinState.editing = on;
    $("#opt-edit").checked = on;
    editbar.hidden = !on;
    document.body.classList.toggle("editing", on);
    placing = null;
    if (on) { fillPlaceSelect(); saveEdits(); }
    applyPinState();
  }
  map.on("click", (e) => {
    if (!pinState.editing || !placing) return;
    const { id, note } = placing;
    placing = null;
    if (places[id]) places[id].offmap = null;
    edits[id] = note ? { note, map: current, at: xy(e.latlng) } : { map: current, at: xy(e.latlng) };
    applyEdit(id, edits[id]);
    saveEdits();
    fillPlaceSelect();
    applyPinState();
  });
  editbar.addEventListener("click", async (e) => {
    const act = e.target.closest("button")?.dataset.act;
    if (act === "done") setEditing(false);
    if (act === "reset") {
      for (const id of Object.keys(edits)) {
        if (extraByKey[id]) { applyEdit(id, { at: extraByKey[id].at }); continue; }
        const o = original[id] || {};
        if (o.at) applyEdit(id, o);
        else if (markers[id]) {
          for (const lyr of Object.values(layers)) lyr.pins.removeLayer(markers[id]);
          delete markers[id];
          if (places[id].isNew) delete places[id];
          else Object.assign(places[id], o);
        }
      }
      edits = {};
      saveEdits();
      fillPlaceSelect();
      applyPinState();
    }
    if (act === "publish") {
      if (!Object.keys(edits).length) { editStatus.textContent = "Ingen ændringer at gemme."; return; }
      // Opens GitHub's "new file" page with the moves filled in; committing it starts .github/workflows/apply-moves.yml.
      const stamp = new Date().toISOString().replace(/\D/g, "").slice(0, 14);
      const url = `https://github.com/${REPO}/new/main?filename=${encodeURIComponent(`moves/${stamp}.json`)}`
        + `&value=${encodeURIComponent(JSON.stringify(edits, null, 1))}`;
      window.open(url, "_blank", "noopener");
      editStatus.textContent = "Tryk \u201cCommit changes\u201d på GitHub. Kortet er opdateret for alle efter et par minutter.";
    }
    if (act === "copy") {
      const text = JSON.stringify(edits, null, 1);
      editExport.value = text;
      editExport.hidden = false;
      editExport.select();
      try { await navigator.clipboard.writeText(text); editStatus.textContent = "Kopieret – indsæt det i chatten."; }
      catch { editStatus.textContent = "Markér teksten herunder og kopiér den."; }
    }
  });
  $("#opt-edit").addEventListener("change", (e) => setEditing(e.target.checked));
  for (const [id, e] of Object.entries(edits)) applyEdit(id, e);

  // ---------- Note reader (#note/<id>) ----------
  let notes = null;
  const loadNotes = () => (notes ||= fetch(`data/notes.json${V}`).then((r) => r.json()));
  const GROUP_ORDER = ["Sessioner", "Gruppen", "Steder", "Personer", "Factions", "Karakterer", "Missioner", "Krønike",
    "Hemmeligheder", "Eventyr", "Sessionsnoter", "Handouts", "Genstande", "Loot", "Journal", "Lore", "Bibel",
    "Skyggekompagniet", "Spillernes vault", "Forberedelse", "Idéer", "Lister", "Regler", "Andet"];
  const sessionOrder = (n) => n.session ?? Infinity;


  const noteHref = (all, k) => (all[k]?.session != null && sessionByNum(all[k].session)
    ? `#session/${all[k].session}/laes` : `#note/${k}`);

  async function showNote(id) {
    const all = await loadNotes();
    // A party member without a note of their own gets an empty note, so the card is still shown.
    const n = all[id] || (people[id]?.noNote ? { title: people[id].name, group: "Personer", md: "", links: [], backlinks: [] } : null);
    if (!n) return closePanel();
    // Reading a session log with Rejsen open moves the journey there too, whichever link led here
    // (related box, "Next Session" links in the text, back button).
    const sIdx = n.session != null ? sessions.indexOf(sessionByNum(n.session)) : -1;
    if (sIdx >= 0 && (jBody.hidden || sIdx !== step)) showSession(sIdx, true);
    const related = [...new Set([...n.links, ...n.backlinks])].filter((k) => all[k]);
    const groups = GROUP_ORDER.map((g) => [g, related.filter((k) => all[k].group === g)
      .sort((a, b) => sessionOrder(all[a]) - sessionOrder(all[b]) || all[a].title.localeCompare(all[b].title, "da"))])
      .filter(([, ids]) => ids.length);
    const label = (k) => (all[k].session != null ? `${UNIT} ${all[k].session}` : all[k].title);
    const [placeKind, placeId] = n.place || [];
    const s = n.session != null ? sessionByNum(n.session) : null;

    const person = people[id];
    const card = person ? el("div", { class: "person-card" },
      monogram(id, true),
      el("div", {},
        el("div", { class: "badges" },
          el("span", { class: `badge stance-${person.stance}` }, STANCE[person.stance]),
          person.pc ? el("span", { class: "badge pc" }, "Gruppen") : null,
          person.dead ? el("span", { class: "badge", title: person.statusNote || null }, "Død †") : person.status ? el("span", { class: "badge" }, statusText(person.status)) : null),
        person.statusNote ? el("p", { class: "person-facts where" }, person.statusNote) : null,
        el("p", { class: "person-facts" }, [person.race, person.social, person.role].filter(Boolean).join(" · ") || null),
        person.pc
          ? el("p", { class: "person-facts" }, person.dead ? "Rejste med gruppen" : "Rejser med gruppen",
              person.origin ? [" · Fra: ", el("a", { href: `#${placeRoute(person.origin)}` }, placeName(person.origin))] : null)
          : el("p", { class: "person-facts" }, "Opholdssted: ",
              person.place ? el("a", { href: `#${placeRoute(person.place)}` }, placeName(person.place)) : "ukendt",
              person.place && person.placeGuess ? el("small", { class: "guess" }, " (udledt af noten)") : null),
        person.factions.length ? el("p", { class: "person-facts" }, "Factions: ",
          person.factions.flatMap((f, i) => [i ? ", " : null, el("a", { href: `#note/${f}` }, factions[f].name)])) : null,
        person.sessions.length ? sessionChips(person) : null)) : null;

    const faction = factions[id];
    let influenceBtn = null;
    if (faction) {
      influenceBtn = el("button", { type: "button", class: "note-link influence-btn", onclick: () => {
        if (pinState.lit) { clearInfluence(); select(null); influenceBtn.textContent = "Vis indflydelse på kortet"; }
        else if (showInfluence(id)) influenceBtn.textContent = "Skjul indflydelse";
        else influenceBtn.textContent = "Ingen kendte steder";
      } }, "Vis indflydelse på kortet");
    }
    const members = faction ? [...faction.members].sort(byName) : [];
    const memberList = el("ul", { class: "people-list" }, members.slice(0, 8).map((k) => personRow(k, true)));
    const fcard = faction ? el("div", { class: "person-card" },
      banner(id, true),
      el("div", {},
        el("div", { class: "badges" },
          el("span", { class: `badge stance-${faction.stance}` }, STANCE[faction.stance]),
          faction.status && faction.status !== "unknown" ? el("span", { class: "badge" }, statusText(faction.status)) : null),
        faction.type ? el("p", { class: "person-facts" }, ftype(faction.type)) : null,
        faction.seat ? el("p", { class: "person-facts" }, "Sæde: ", el("a", { href: `#${placeRoute(faction.seat)}` }, placeName(faction.seat)),
          faction.seatGuess ? el("small", { class: "guess" }, " (udledt af noten)") : null) : null,
        faction.leader.length ? el("p", { class: "person-facts" }, "Leder: ",
          faction.leader.flatMap((k, i) => [i ? ", " : null, el("a", { href: `#note/${k}` }, people[k]?.name || k)])) : null,
        faction.sessions.length ? el("div", { class: "chips" }, faction.sessions.map((num) =>
          el("a", { class: "session-link", href: `#session/${num}/laes` }, `${UNIT} ${num}`))) : null,
        influenceBtn)) : null;
    const memberSection = members.length ? [el("h3", {}, `Medlemmer (${members.length})`), memberList,
      members.length > 8 ? el("button", { type: "button", class: "more",
        onclick: (e) => { memberList.append(...members.slice(8).map((k) => personRow(k, true))); e.target.remove(); } }, `Vis alle ${members.length}`) : null] : null;
    markSessions(person?.sessions || faction?.sessions || []);

    const text = el("div", { class: "note-md" });
    text.innerHTML = marked.parse(n.md);
    for (const a of text.querySelectorAll("a[href^='http']")) { a.target = "_blank"; a.rel = "noopener"; }
    for (const a of text.querySelectorAll("a[href^='#note/']")) a.setAttribute("href", noteHref(all, a.getAttribute("href").slice(6)));
    // "### Session 44 – …" headings link to that session, like the timeline's numbers.
    for (const h of text.querySelectorAll("h1, h2, h3, h4, h5, h6")) {
      const m = h.textContent.match(/^\s*Session\s+(\d+(?:\.\d+)?)\b/i);
      if (m && sessionByNum(m[1]) && !h.querySelector("a")) {
        const a = el("a", { href: `#session/${sessionByNum(m[1]).num}/laes`, class: "heading-link" });
        a.append(...h.childNodes);
        h.append(a);
      }
    }

    openPanel(
      el("p", { class: "kicker" }, n.group === "Sessioner" ? "Sessionslog" : person?.pc ? "Gruppen" : n.group),
      el("h2", {}, s ? `${UNIT} ${s.num}: ${s.title}` : n.title + (person?.dead ? " †" : "")),
      card,
      fcard,
      memberSection,
      n.together?.length ? el("div", { class: "together" }, el("h4", {}, "Nævnt i de samme sessioner som"),
        el("ul", { class: "chips" }, n.together.filter(([k]) => all[k]).map(([k, c]) =>
          el("li", {}, el("a", { href: `#note/${k}`, title: `${c} fælles sessioner` }, all[k].title, el("small", {}, ` ${c}`)))))) : null,
      el("div", { class: "note-actions" },
        placeKind ? el("a", { class: "note-link", href: `#${placeKind}/${placeId}` }, "Vis på kortet") : null,
        s && jBody.hidden ? el("a", { class: "note-link", href: `#session/${s.num}` }, "Vis i Rejsen") : null),
      groups.length ? el("details", { class: "related" },
        el("summary", {}, `Relaterede noter (${related.length})`),
        groups.map(([g, ids]) => el("div", { class: "related-group" },
          el("h4", {}, g),
          el("ul", { class: "chips" }, ids.map((k) => el("li", {}, el("a", { href: noteHref(all, k), title: all[k].title }, label(k)))))))) : null,
      text,
    );
    panel.classList.add("wide");
    if (placeKind === "sted") { focusPin(placeId); select(anchor(placeId)); }
    // A person's note shows where they live.
    const home = person?.place;
    if (home && !home.startsWith("region:") && places[home]) { focusPin(home); select(anchor(home)); }
  }

  // ---------- Tråde and tracking tools (#traade, #traade/<view>, #traad/<id>) ----------
  // Threads are hand-written in docs/traade.md; the tools only list what the logs say.
  const VIEWS = [["", "Tråde"], ["glemte", "Glemte"], ["naeste", "Næste skridt"], ["spoergsmaal", "Spørgsmål"]];
  const sessionLink = (num) => el("a", { class: "session-link", href: `#session/${num}/laes` }, `S${num}`);
  const md = (text, inline = false) => {
    const n = el(inline ? "span" : "div", { class: inline ? "" : "note-md thread-md" });
    n.innerHTML = inline ? marked.parseInline(text) : marked.parse(text);
    return n;
  };
  function threadsHeader(view) {
    for (const b of tabs.children) b.setAttribute("aria-pressed", String(b.dataset.map === "traade"));
    return [
      el("p", { class: "kicker" }, "Tråde og spor"),
      el("h2", {}, VIEWS.find(([k]) => k === view)[1]),
      el("nav", { class: "segments", "aria-label": "Visning" }, VIEWS.map(([k, label]) =>
        el("a", { href: `#traade${k ? "/" + k : ""}`, "aria-current": String(k === view) }, label))),
    ];
  }
  const firstText = (t) => {
    const part = t.parts.find(([l]) => l === "Status") || t.parts.find(([l]) => l === "Åbent") || t.parts[0];
    return part ? part[1].replace(/\[([^\]]+)\]\([^)]*\)/g, "$1").replace(/[*`_]/g, "").split("\n")[0] : "";
  };
  function showThreads(view = "") {
    const body = [];
    if (view === "") {
      const groups = [...new Set(threads.map((t) => t.group))];
      body.push(el("p", { class: "dir-count" }, "Skrevet ud fra alle sessionslogs. Hvert spor linker til sin session."));
      for (const g of groups) {
        body.push(el("h3", {}, g), el("ul", { class: "thread-list" }, threads.filter((t) => t.group === g).map((t) =>
          el("li", {}, el("a", { href: `#traad/${t.id}` }, el("b", {}, t.title), el("small", {}, firstText(t)))))));
      }
    } else if (view === "glemte") {
      body.push(el("p", { class: "dir-count" },
        `Nævnt i mindst to sessioner, men ikke siden session ${tools.latest - 12}. Døde personer er udeladt, når noten siger det.`));
      const KINDS = { People: "Person", Locations: "Sted", Factions: "Faction", Items: "Genstand", Loot: "Loot" };
      body.push(el("ul", { class: "thread-list" }, tools.forgotten.map((f) => el("li", {},
        el("a", { href: `#note/${f.id}` }, el("b", {}, f.title),
          el("small", {}, `${KINDS[f.kind] || f.kind} · nævnt i ${f.sessions.length} sessioner · sidst i session ${f.last}`))))));
    } else if (view === "naeste") {
      body.push(el("p", { class: "dir-count" }, "Gruppens egne NEXT-linjer fra loggene, nyeste først."));
      body.push(...[...tools.next].reverse().map((x, i) => el("section", { class: `next-step${i === 0 ? " latest" : ""}` },
        el("h4", {}, i === 0 ? "Seneste · " : "", sessionLink(x.session), " ", sessionByNum(x.session)?.title || ""),
        el("ul", {}, x.items.map((it) => el("li", {}, it))))));
    } else if (view === "spoergsmaal") {
      body.push(el("p", { class: "dir-count" }, "Spørgsmål I selv har skrevet i loggene."));
      body.push(el("ul", { class: "thread-list" }, tools.questions.map((q) =>
        el("li", {}, el("span", {}, q.text), el("small", {}, sessionLink(q.session))))));
    }
    openPanel(...threadsHeader(view), ...body);
    panel.classList.add("wide");
  }
  // Places and people named in a thread, found by name in its text.
  function threadMentions(t) {
    const text = fold(t.parts.map(([, x]) => x.replace(/\([^)]*\)/g, "")).join(" "));
    const has = (name) => name.length >= 5 && new RegExp(`(^|[^a-z0-9])${fold(name).replace(/[.*+?^${}()|[\]\\]/g, "\\$&")}([^a-z0-9]|$)`).test(text);
    const pl = Object.keys(places).filter((k) => [places[k].name, ...places[k].aliases].some(has));
    const pp = Object.keys(people).filter((k) => [people[k].name, ...people[k].aliases].some(has));
    return [pl, pp];
  }
  // Place and region names in a short text become links to their notes ("Astley og Welles").
  const nameLinks = (() => {
    const out = [];
    for (const p of Object.values(places)) if (p.noteId) [p.name, ...p.aliases].forEach((n) => out.push([n, p.noteId]));
    for (const r of Object.values(regions)) if (r.noteId) {
      out.push([r.name, r.noteId]);
      out.push([r.name.split(" ").pop(), r.noteId]); // "Baroniet Welles" -> "Welles"
    }
    return out.filter(([n]) => n.length >= 4).sort((a, b) => b[0].length - a[0].length);
  })();
  function linkNames(text) {
    for (const [name, id] of nameLinks) {
      const i = text.search(new RegExp(`(^|[^\\wæøå])${name.replace(/[.*+?^${}()|[\]\\]/g, "\\$&")}(?![\\wæøå])`));
      if (i < 0) continue;
      const start = text.indexOf(name, i);
      return [...linkNames(text.slice(0, start)), el("a", { href: `#note/${id}` }, name), ...linkNames(text.slice(start + name.length))];
    }
    return text ? [text] : [];
  }

  function showThread(id) {
    const t = threads.find((x) => x.id === id);
    if (!t) return showThreads();
    for (const b of tabs.children) b.setAttribute("aria-pressed", String(b.dataset.map === "traade"));
    const [pl, pp] = threadMentions(t);
    openPanel(
      el("p", { class: "crumbs" }, el("a", { href: "#traade" }, "Tråde"), " › ", ...linkNames(t.group)),
      el("h2", {}, t.title),
      t.parts.map(([label, text]) => el("section", { class: `thread-part${label === "Muligt (gæt)" ? " guess" : ""}` },
        label ? el("h3", {}, label) : null, md(text))),
      pl.length ? [el("h3", {}, "Steder"), el("ul", { class: "chips" }, pl.map((k) =>
        el("li", {}, el("a", { href: `#sted/${k}` }, places[k].name))))] : null,
      pp.length ? [el("h3", {}, "Personer"), el("ul", { class: "people-list" }, pp.map((k) => personRow(k, true)))] : null,
    );
    panel.classList.add("wide");
  }

  // ---------- Routing (#sted/astley, #region/welles, #session/12, #kort/nordheim) ----------
  function go(route) {
    if (location.hash.slice(1) === route) route_(route);
    else location.hash = route;
  }
  function route_(hash) {
    const [kind, id, sub] = decodeURIComponent(hash).split("/");
    clearInfluence();
    if (kind !== "session" && !(kind === "note" && !jBody.hidden)) { stopPlay(); endJourney(); }
    if (kind === "sted" && places[id]) showPlace(id);
    else if (kind === "region" && regions[id]) showRegion(id);
    else if (kind === "session" && sessionByNum(id)) {
      showSession(sessions.indexOf(sessionByNum(id)), sub === "laes");
      if (sub === "laes" && sessionByNum(id).noteId) showNote(sessionByNum(id).noteId);
    }
    else if (kind === "note") showNote(id);
    else if (kind === "personer") showDirectory(id || "");
    else if (kind === "traade") showThreads(VIEWS.some(([k]) => k === (id || "")) ? id || "" : "");
    else if (kind === "traad") showThread(id);
    else if (kind === "udenfor" && offmap[id]) showOffmap(id);
    else if (kind === "kort" && maps[id]) showMapPanel(id);
    else { closePanel(); showMap(current || campaign.start, !current); }
  }
  window.addEventListener("hashchange", () => route_(location.hash.slice(1)));
  document.addEventListener("keydown", (e) => {
    if (e.key === "Escape" && !panel.hidden && document.activeElement !== input) go(closeRoute());
  });

  if (!sessions.length) journey.style.display = "none";
  // The GM's edition shows everything; mark it so it is never mistaken for the players' site.
  if (campaign.audience === "gm") {
    document.body.classList.add("gm-view");
    $(".cartouche h1").append(el("span", { class: "gm-badge" }, "GM"));
    document.title += " – GM";
  }
  showMap(campaign.start);
  route_(location.hash.slice(1));
})();
