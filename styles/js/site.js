// Wuji — le peu de script du site. Tout ce qu'il fait est un confort : sans lui, chaque page se
// lit en entier, le menu du téléphone reste accessible par le pied de page, et les deux
// signes des touches qui changent d'un clavier à l'autre s'affichent côte à côte.

(() => {
  const racine = document.documentElement;

  // ── Le clavier : AZERTY ou QWERTY ─────────────────────────────────────────────
  // macOS adapte les raccourcis des menus à la disposition du clavier : ⌘] se tape avec la
  // touche à droite du P, qui porte « $ » sur un clavier français. On montre donc les signes
  // de votre clavier — deviné d'après la langue du navigateur, puis retenu si vous choisissez.
  const clé = 'wuji.clavier';
  const lire = () => { try { return localStorage.getItem(clé); } catch { return null; } };
  const écrire = (v) => { try { localStorage.setItem(clé, v); } catch { /* navigation privée */ } };
  const deviné = (navigator.language || '').toLowerCase().startsWith('fr') ? 'azerty' : 'qwerty';
  const poser = (clavier) => {
    racine.classList.remove('k-azerty', 'k-qwerty');
    racine.classList.add('k-' + clavier);
    for (const b of document.querySelectorAll('[data-layout]')) {
      b.setAttribute('aria-pressed', String(b.dataset.layout === clavier));
    }
  };
  poser(lire() || deviné);
  document.addEventListener('click', (ev) => {
    const b = ev.target.closest('[data-layout]');
    if (!b) return;
    écrire(b.dataset.layout);
    poser(b.dataset.layout);
  });

  // ── La barre : un filet dès qu'on a quitté le haut, et le menu du téléphone ───
  const barre = document.querySelector('.nav');
  if (barre) {
    const suivre = () => barre.classList.toggle('scrolled', window.scrollY > 4);
    suivre();
    window.addEventListener('scroll', suivre, { passive: true });
    const bouton = barre.querySelector('.nav-toggle');
    bouton?.addEventListener('click', () => {
      const ouvert = barre.classList.toggle('open');
      bouton.setAttribute('aria-expanded', String(ouvert));
    });
    document.addEventListener('keydown', (ev) => {
      if (ev.key === 'Escape' && barre.classList.contains('open')) {
        barre.classList.remove('open');
        bouton?.setAttribute('aria-expanded', 'false');
      }
    });
  }

  // ── Le sommaire de la page suit la lecture ────────────────────────────────────
  const liens = [...document.querySelectorAll('.toc-page a[href^="#"]')];
  if (liens.length && 'IntersectionObserver' in window) {
    const parId = new Map(liens.map((a) => [a.getAttribute('href').slice(1), a]));
    const visibles = new Set();
    const marquer = () => {
      const premier = [...parId.keys()].find((id) => visibles.has(id));
      for (const [id, a] of parId) a.classList.toggle('here', id === premier);
    };
    const observateur = new IntersectionObserver((entrées) => {
      for (const e of entrées) e.isIntersecting ? visibles.add(e.target.id) : visibles.delete(e.target.id);
      marquer();
    }, { rootMargin: '-20% 0px -55% 0px' });
    for (const id of parId.keys()) {
      const section = document.getElementById(id);
      if (section) observateur.observe(section);
    }
  }

  // ── La visionneuse : une capture s'agrandit au clic ───────────────────────────
  const images = document.querySelectorAll('img[data-zoom]');
  if (images.length && 'HTMLDialogElement' in window) {
    const boîte = document.createElement('dialog');
    boîte.className = 'lightbox';
    const grande = document.createElement('img');
    boîte.append(grande);
    document.body.append(boîte);
    for (const img of images) {
      img.addEventListener('click', () => {
        grande.src = img.currentSrc || img.src;
        grande.alt = img.alt;
        boîte.showModal();
      });
    }
    boîte.addEventListener('click', () => boîte.close());
  }
})();
