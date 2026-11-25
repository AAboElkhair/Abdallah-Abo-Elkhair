/* A+ MQ - the one signup form: book a demo, or (with an invitation code) download the trial.

   Without a code: the details go to the author (FormSubmit e-mail, and the signup server when there is one).
   With a code ("I have an invitation code" ticked): the code unlocks the trial setup, which is published only encrypted
   (trial/a-plus-mq-trial.bin). The file key comes either
     - from the signup server (form data-api set): it checks the code, records the signup and returns the key; or
     - with no server yet: from trial/keys.json, where the key is wrapped once per code (PBKDF2-SHA256 + AES-GCM).
   The setup is decrypted here, its SHA-256 checked, then saved. Made with the AAMQ repository's DevTools\TrialPack and AAMQ\Server. */
(function () {
  var f = document.getElementById('demo-form');
  if (!f) return;
  var ar = document.documentElement.lang === 'ar';
  var T = ar ? {
    nocrypto: 'المتصفح ده ما بيدعمش التحميل الآمن. جرّب Chrome أو Edge أو Firefox بنسخة حديثة.',
    bad: 'الكود ده مش صحيح أو اتلغى. اتأكد منه، أو اطلب كود من المؤلف.',
    many: 'محاولات كتير. استنى شوية وجرّب تاني.',
    check: 'بنتأكد من الكود...', get: 'بنحمّل الملف...', open: 'بنفك الملف...',
    net: 'التحميل ما كملش. اتأكد من النت وجرّب تاني.', hash: 'الملف وصل ناقص أو متغيّر. جرّب تاني.'
  } : {
    nocrypto: 'This browser cannot do the secure download. Please use a recent Chrome, Edge or Firefox.',
    bad: 'This invitation code is not valid or was withdrawn. Check it, or ask the author for a code.',
    many: 'Too many tries. Please wait a little and try again.',
    check: 'Checking your code...', get: 'Downloading...', open: 'Unlocking the file...',
    net: 'The download did not finish. Check your connection and try again.', hash: 'The file arrived incomplete or changed. Please try again.'
  };
  var cb = document.getElementById('has-code'), box = document.getElementById('code-box');
  var codeIn = f.querySelector('[name=Code]'), btn = f.querySelector('button[type=submit]');
  var er = f.querySelector('.ferr'), erMsg = er.querySelector('span'), erDefault = erMsg.textContent;
  var subj = f.querySelector('[name=_subject]'), subjDemo = subj.value;
  var api = (f.getAttribute('data-api') || '').replace(/\/+$/, ''), base = f.getAttribute('data-base') || 'trial/';
  var lastUrl = null, lastName = null;

  // ---- the checkbox: shows the code field and turns the button into "Register and download"
  function mode() {
    var on = cb.checked;
    box.hidden = !on;
    codeIn.required = on;
    btn.textContent = on ? btn.getAttribute('data-dl') : btn.getAttribute('data-demo');
    subj.value = on ? btn.getAttribute('data-dl-subject') : subjDemo;
    er.hidden = true;
  }
  cb.addEventListener('change', function () { mode(); if (cb.checked) codeIn.focus(); });
  mode();

  // ---- helpers
  function b64(s) { var b = atob(s), u = new Uint8Array(b.length); for (var i = 0; i < b.length; i++) u[i] = b.charCodeAt(i); return u; }
  function hex(buf) { return Array.prototype.map.call(new Uint8Array(buf), function (x) { return ('0' + x.toString(16)).slice(-2); }).join(''); }
  function norm(c) { var s = (c || '').toUpperCase().replace(/[^A-Z0-9]/g, ''); return s.indexOf('AMQ') === 0 ? s.slice(3) : s; }
  function label() { return cb.checked ? btn.getAttribute('data-dl') : btn.getAttribute('data-demo'); }
  function busy(msg) { btn.disabled = true; btn.textContent = msg; }
  function fail(msg, withMail) {
    erMsg.textContent = msg || erDefault;
    er.querySelector('a').hidden = !withMail;
    er.hidden = false; btn.disabled = false; btn.textContent = label();
  }
  function show(id) { f.hidden = true; var ok = document.getElementById(id); ok.hidden = false; ok.scrollIntoView({ block: 'center' }); }
  function save() { var a = document.createElement('a'); a.href = lastUrl; a.download = lastName; document.body.appendChild(a); a.click(); a.remove(); }
  function fields(withCode) {
    var d = {};
    new FormData(f).forEach(function (v, k) { d[k] = v; });
    if (!withCode) delete d.Code;
    return d;
  }
  // wait: ms before giving up (a network that blocks the server can hang for a minute otherwise)
  function post(url, d, wait) {
    var o = { method: "POST", headers: { 'Content-Type': 'application/json', 'Accept': 'application/json' }, body: JSON.stringify(d) };
    if (wait && window.AbortController) { var ac = new AbortController(); o.signal = ac.signal; setTimeout(function () { ac.abort(); }, wait); }
    return fetch(url, o);
  }
  // the author's e-mail copy (FormSubmit): resolves true when it was accepted
  function mail(d) {
    return post(f.getAttribute('data-ajax'), d)
      .then(function (r) { return r.json().then(function (j) { return r.ok && String(j.success) !== 'false'; }); })
      .catch(function () { return false; });
  }
  // the signup server: resolves the Response, or null when there is no server or it cannot be reached
  function server(d) {
    if (!api) return Promise.resolve(null);
    return post(api + "/api/signup", d, 10000).catch(function () { return null; });
  }

  function fetchBin(url, size) {
    return fetch(url, { cache: 'no-store' }).then(function (r) {
      if (!r.ok) throw 'net';
      if (!r.body || !r.body.getReader) return r.arrayBuffer();
      var rd = r.body.getReader(), parts = [], got = 0;
      function pump() {
        return rd.read().then(function (x) {
          if (x.done) { var all = new Uint8Array(got), o = 0; parts.forEach(function (p) { all.set(p, o); o += p.length; }); return all.buffer; }
          parts.push(x.value); got += x.value.length;
          if (size) btn.textContent = T.get + ' ' + Math.min(99, Math.round(got * 100 / (size + 32))) + '%';
          return pump();
        });
      }
      return pump();
    });
  }

  // ---- the file key for a code: { key: CryptoKey, rel: {file, name, size, sha256} }
  function keyFromServer(c, d) {
    return server(d).then(function (r) {
      if (!r) throw 'net';
      if (r.status === 403) throw 'bad';
      if (r.status === 429) throw 'many';
      if (!r.ok) throw 'net';
      return r.json();
    }).then(function (j) {
      return c.importKey('raw', b64(j.release.key), 'AES-GCM', false, ['decrypt']).then(function (k) { return { key: k, rel: j.release }; });
    });
  }
  function keyFromStatic(c, n) {
    var enc = new TextEncoder(), man;
    return fetch(base + 'keys.json', { cache: 'no-store' }).then(function (r) { if (!r.ok) throw 'net'; return r.json(); })
      .then(function (m) { man = m; return c.digest('SHA-256', enc.encode('aamq-trial:' + n)); })
      .then(function (h) {
        var k = man.keys[hex(h).slice(0, 16)];
        if (!k) throw 'bad';
        return c.importKey('raw', enc.encode(n), 'PBKDF2', false, ['deriveKey'])
          .then(function (pw) { return c.deriveKey({ name: 'PBKDF2', salt: b64(k.s), iterations: man.iter, hash: 'SHA-256' }, pw, { name: 'AES-GCM', length: 256 }, false, ['decrypt']); })
          .then(function (kek) { return c.decrypt({ name: 'AES-GCM', iv: b64(k.i) }, kek, b64(k.k)); })
          .catch(function () { throw 'bad'; });
      })
      .then(function (raw) { return c.importKey('raw', raw, 'AES-GCM', false, ['decrypt']); })
      .then(function (k) { return { key: k, rel: man }; });
  }

  function download(d) {
    var c = window.crypto && window.crypto.subtle;
    if (!c || !window.TextEncoder) return fail(T.nocrypto);
    var n = norm(d.Code);
    if (n.length !== 12) return fail(T.bad);
    var got;
    busy(T.check);
    // a network that blocks the server (some offices block *.workers.dev) falls back to keys.json
    (api ? keyFromServer(c, d).catch(function (x) { if (x === "net") return keyFromStatic(c, n); throw x; }) : keyFromStatic(c, n))
      .then(function (k) {
        got = k;
        mail(d);                      // the author's e-mail copy; a missed e-mail does not stop a valid download
        busy(T.get);
        return fetchBin(base + got.rel.file, got.rel.size);
      })
      .then(function (buf) {
        busy(T.open);
        var u = new Uint8Array(buf);
        if (String.fromCharCode(u[0], u[1], u[2], u[3]) !== 'AMQ1') throw 'hash';
        return c.decrypt({ name: 'AES-GCM', iv: u.slice(4, 16) }, got.key, u.slice(16)).catch(function () { throw 'hash'; });
      })
      .then(function (file) {
        return c.digest('SHA-256', file).then(function (h) {
          if (hex(h) !== got.rel.sha256) throw 'hash';
          var exe = /[.]exe$/i.test(got.rel.name);
          lastUrl = URL.createObjectURL(new Blob([file], { type: exe ? 'application/octet-stream' : 'application/zip' }));
          lastName = got.rel.name;
          save();
          show('trial-ok');
        });
      })
      .catch(function (x) { fail(x === 'bad' ? T.bad : x === 'many' ? T.many : x === 'hash' ? T.hash : T.net); });
  }

  function demo(d) {
    busy(btn.getAttribute('data-sending'));
    Promise.all([server(d), mail(d)]).then(function (r) {
      var saved = r[0] && r[0].ok, mailed = r[1];
      if (saved || mailed) return show('demo-ok');
      // last resort: the plain FormSubmit post (it shows its own page and comes back to #demo)
      try { HTMLFormElement.prototype.submit.call(f); } catch (x) { fail(null, true); }
    });
  }

  f.addEventListener('submit', function (e) {
    if (!window.fetch) return;           // very old browser: the plain form post to FormSubmit
    e.preventDefault();
    er.hidden = true;
    if (!f.reportValidity()) return;
    if (f.querySelector('[name=_honey]').value) return show('demo-ok');
    var withCode = cb.checked, d = fields(withCode);
    if (withCode) download(d); else demo(d);
  });

  var again = document.getElementById('trial-again');
  if (again) again.addEventListener('click', function (e) { e.preventDefault(); if (lastUrl) save(); });
})();
