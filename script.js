async function loadProfile() {
  const res = await fetch('content.json');
  const data = await res.json();

  // ---- Hero ----
  document.getElementById('hero-name').textContent = data.name;
  document.getElementById('hero-subtitle').textContent = data.heroSubtitle;
  document.title = data.name + ' — Executive Profile';

  // ---- Executive Profile (with photo) ----
  const narrative = document.getElementById('profile-narrative');
  const [lead, ...rest] = data.executiveProfile;
  const leadCol = document.createElement('div');
  const leadP = document.createElement('p');
  leadP.className = 'lead-p';
  leadP.textContent = lead;
  leadCol.appendChild(leadP);

  const bodyCol = document.createElement('div');
  rest.forEach(paragraph => {
    const p = document.createElement('p');
    p.className = 'body-p';
    p.textContent = paragraph;
    bodyCol.appendChild(p);
  });
  narrative.appendChild(leadCol);
  narrative.appendChild(bodyCol);

  if (data.photo && data.photo.url) {
    const photoBox = document.getElementById('profile-photo');
    photoBox.innerHTML = '';
    const img = document.createElement('img');
    img.src = data.photo.url;
    img.alt = data.name;
    photoBox.appendChild(img);
  }

  // ---- Strategic Value Drivers ----
  const drivers = document.getElementById('drivers-grid');
  data.strategicValueDrivers.forEach((d, i) => {
    const card = document.createElement('div');
    card.className = 'driver-card';
    card.innerHTML = `
      <span class="driver-index">0${i + 1}</span>
      <h3 class="driver-title"></h3>
      <p class="driver-desc"></p>
    `;
    card.querySelector('.driver-title').textContent = d.title;
    card.querySelector('.driver-desc').textContent = d.desc;
    drivers.appendChild(card);
  });

  // ---- Sector Footprint (full role history, current + former) ----
  const footprint = document.getElementById('footprint-list');
  data.sectorFootprint.forEach(f => {
    const item = document.createElement('div');
    item.className = 'footprint-item';

    const titleWrap = document.createElement('div');
    const titleEl = document.createElement('h3');
    titleEl.className = 'footprint-title';
    titleEl.textContent = f.title;
    titleWrap.appendChild(titleEl);
    if (!f.current) {
      const tag = document.createElement('span');
      tag.className = 'former-tag';
      tag.textContent = 'Former';
      titleWrap.appendChild(tag);
    }
    const roleEl = document.createElement('span');
    roleEl.className = 'footprint-role';
    roleEl.textContent = `${f.org} · ${f.period}`;
    titleWrap.appendChild(document.createElement('br'));
    titleWrap.appendChild(roleEl);

    const descEl = document.createElement('div');
    descEl.className = 'footprint-desc';
    const strong = document.createElement('strong');
    strong.textContent = f.role;
    descEl.appendChild(strong);
    descEl.appendChild(document.createTextNode(' — ' + f.detail));

    item.appendChild(titleWrap);
    item.appendChild(descEl);
    footprint.appendChild(item);
  });

  // ---- Education & Executive Development ----
  const edu = document.getElementById('edu-grid');
  data.education.forEach(e => {
    const li = document.createElement('li');
    li.innerHTML = `<strong></strong><span></span>`;
    li.querySelector('strong').textContent = e.institution;
    li.querySelector('span').textContent = e.credential;
    edu.appendChild(li);
  });

  // ---- Recognition ----
  const rec = document.getElementById('recognition-list');
  data.recognition.forEach(r => {
    const row = document.createElement('div');
    row.className = 'rec-item';
    const award = document.createElement('span');
    award.className = 'rec-award';
    award.textContent = r.award;
    const meta = document.createElement('span');
    meta.className = 'rec-meta';
    meta.textContent = r.issuer ? `${r.year}, ${r.issuer}` : r.year;
    row.appendChild(award);
    row.appendChild(meta);
    rec.appendChild(row);
  });

  // ---- Contact ----
  const contactBox = document.getElementById('contact-copy');
  const c = data.contact;
  const mainSiteDisplay = c.mainSite.replace(/^https?:\/\//, '');

  const line1 = document.createElement('p');
  line1.appendChild(document.createTextNode('For strategic collaborations, direct advisory, or general corporate matters, please direct all communication to '));
  const emailLink = document.createElement('a');
  emailLink.href = 'mailto:' + c.businessEmail;
  emailLink.textContent = c.businessEmail;
  line1.appendChild(emailLink);
  line1.appendChild(document.createTextNode('.'));

  const line2 = document.createElement('p');
  line2.appendChild(document.createTextNode('To explore ongoing philanthropic initiatives, personal foundation work, and broader venture investments, visit '));
  const siteLink = document.createElement('a');
  siteLink.href = c.mainSite;
  siteLink.target = '_blank';
  siteLink.rel = 'noopener';
  siteLink.textContent = mainSiteDisplay;
  line2.appendChild(siteLink);
  line2.appendChild(document.createTextNode('.'));

  const line3 = document.createElement('p');
  line3.appendChild(document.createTextNode('You can also connect professionally via '));
  const liLink = document.createElement('a');
  liLink.href = c.linkedin;
  liLink.target = '_blank';
  liLink.rel = 'noopener';
  liLink.textContent = 'LinkedIn';
  line3.appendChild(liLink);
  line3.appendChild(document.createTextNode('.'));

  contactBox.appendChild(line1);
  contactBox.appendChild(line2);
  contactBox.appendChild(line3);

  // ---- schema.org Person markup (cross-site SEO with seindefadeni.com) ----
  const schema = {
    "@context": "https://schema.org",
    "@type": "Person",
    "name": data.name,
    "jobTitle": "Chairman & Founder",
    "url": window.location.href,
    "sameAs": [c.mainSite, c.linkedin]
  };
  document.getElementById('person-schema').textContent = JSON.stringify(schema, null, 2);
}

loadProfile();
