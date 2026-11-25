/* A+ MQ - code-locked trial download (static page, no server).
   The trial installer is published only encrypted (trial/a-plus-mq-trial.bin). trial/keys.json holds, per access code, the file key
   wrapped with a key derived from that code (PBKDF2-SHA256 + AES-GCM). A valid code unwraps the file key here in the browser,
   the file is decrypted, its SHA-256 checked and saved. The registration goes to the author by FormSubmit (as the demo form).
   Made with the AAMQ repository's DevTools\TrialPack. */
(function () {
  var f = document.getElementById('trial-form');
  if (!f) return;
  var ar = document.documentElement.lang === 'ar';
  var T = ar ? {
    nocrypto: 'المتصفح ده ما بيدعمش التحميل الآمن. جرّب Chrome أو Edge أو Firefox بنسخة حديثة.',
    bad: 'الكود ده مش صحيح. اتأكد منه، أو اطلب كود من المؤلف.',
    check: 'بنتأكد من الكود...', get: 'بنحمّل الملف...', open: 'بنفك الملف...',
    net: 'التحميل ما كملش. اتأكد من النت وجرّب تاني.', hash: 'الملف وصل ناقص أو متغيّر. جرّب تاني.'
  } : {
    nocrypto: 'This browser cannot do the secure download. Please use a recent Chrome, Edge or Firefox.',
    bad: 'This access code is not valid. Check it, or ask the author for a code.',
    check: 'Checking your code...', get: 'Downloading...', open: 'Unlocking the file...',
    net: 'The download did not finish. Check your connection and try again.', hash: 'The file arrived incomplete or changed. Please try again.'
  };
  var base = f.getAttribute('data-base') || 'trial/';
  var btn = f.querySelector('button[type=submit]'), label = btn.textContent, er = f.querySelector('.ferr');
  var lastUrl = null, lastName = null;

  function b64(s) { var b = atob(s), u = new Uint8Array(b.length); for (var i = 0; i < b.length; i++) u[i] = b.charCodeAt(i); return u; }
  function hex(buf) { return Array.prototype.map.call(new Uint8Array(buf), function (x) { return ('0' + x.toString(16)).slice(-2); }).join(''); }
  function norm(c) { var s = (c || '').toUpperCase().replace(/[^A-Z0-9]/g, ''); return s.indexOf('AMQ') === 0 ? s.slice(3) : s; }
  function fail(msg) { er.textContent = msg; er.hidden = false; btn.disabled = false; btn.textContent = label; }
  function busy(msg) { btn.disabled = true; btn.textContent = msg; }
  function save() { var a = document.createElement('a'); a.href = lastUrl; a.download = lastName; document.body.appendChild(a); a.click(); a.remove(); }

  function register(code) {
    var d = {};
    new FormData(f).forEach(function (v, k) { d[k] = v; });
    d.Code = code;
    return fetch(f.getAttribute('data-ajax'), { method: 'POST', headers: { 'Content-Type': 'application/json', 'Accept': 'application/json' }, body: JSON.stringify(d) })
      .catch(function () { /* a missed registration e-mail does not stop a valid download */ });
  }

  function fetchBin(url, size) {
    // with progress where the browser can stream
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

  f.addEventListener('submit', function (e) {
    e.preventDefault();
    er.hidden = true;
    if (!f.reportValidity()) return;
    if (f.querySelector('[name=_honey]').value) return;
    var c = window.crypto && window.crypto.subtle;
    if (!c || !window.fetch || !window.TextEncoder) return fail(T.nocrypto);
    var code = f.querySelector('[name=Code]').value.trim(), n = norm(code);
    if (n.length !== 12) return fail(T.bad);
    var enc = new TextEncoder(), man, fileKey;
    busy(T.check);
    fetch(base + 'keys.json', { cache: 'no-store' }).then(function (r) { if (!r.ok) throw 'net'; return r.json(); })
      .then(function (m) {
        man = m;
        return c.digest('SHA-256', enc.encode('aamq-trial:' + n));
      })
      .then(function (h) {
        var k = man.keys[hex(h).slice(0, 16)];
        if (!k) throw 'bad';
        return c.importKey('raw', enc.encode(n), 'PBKDF2', false, ['deriveKey'])
          .then(function (pw) { return c.deriveKey({ name: 'PBKDF2', salt: b64(k.s), iterations: man.iter, hash: 'SHA-256' }, pw, { name: 'AES-GCM', length: 256 }, false, ['decrypt']); })
          .then(function (kek) { return c.decrypt({ name: 'AES-GCM', iv: b64(k.i) }, kek, b64(k.k)); })
          .catch(function () { throw 'bad'; });
      })
      .then(function (raw) {
        return c.importKey('raw', raw, 'AES-GCM', false, ['decrypt']);
      })
      .then(function (k) {
        fileKey = k;
        register(code);
        busy(T.get);
        return fetchBin(base + man.file, man.size);
      })
      .then(function (buf) {
        busy(T.open);
        var u = new Uint8Array(buf);
        if (String.fromCharCode(u[0], u[1], u[2], u[3]) !== 'AMQ1') throw 'hash';
        return c.decrypt({ name: 'AES-GCM', iv: u.slice(4, 16) }, fileKey, u.slice(16)).catch(function () { throw 'hash'; });
      })
      .then(function (zip) {
        return c.digest('SHA-256', zip).then(function (h) {
          if (hex(h) !== man.sha256) throw 'hash';
          lastUrl = URL.createObjectURL(new Blob([zip], { type: /[.]exe$/i.test(man.name) ? 'application/octet-stream' : 'application/zip' }));
          lastName = man.name;
          save();
          f.hidden = true;
          var ok = document.getElementById('trial-ok');
          ok.hidden = false;
          ok.scrollIntoView({ block: 'center' });
        });
      })
      .catch(function (x) { fail(x === 'bad' ? T.bad : x === 'hash' ? T.hash : T.net); });
  });

  var again = document.getElementById('trial-again');
  if (again) again.addEventListener('click', function (e) { e.preventDefault(); if (lastUrl) save(); });
})();
