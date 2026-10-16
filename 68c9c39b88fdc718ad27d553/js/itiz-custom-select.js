/*
 * Themed dropdowns for the contact page and the side "book a call" form.
 * The native <select> stays in the DOM (visually hidden) so form submission,
 * `required` validation and Webflow form handling keep working unchanged.
 */
(function () {
  'use strict';

  var openInstance = null;
  var uid = 0;

  function enhance(select) {
    if (select.dataset.itizSelect) return;
    select.dataset.itizSelect = '1';

    var wrap = select.parentNode;
    var id = 'itiz-select-' + (++uid);

    var trigger = document.createElement('button');
    trigger.type = 'button';
    trigger.className = 'text-field itiz-select-trigger';
    trigger.id = id + '-trigger';
    trigger.setAttribute('role', 'combobox');
    trigger.setAttribute('aria-haspopup', 'listbox');
    trigger.setAttribute('aria-expanded', 'false');
    trigger.setAttribute('aria-controls', id + '-list');

    var label = select.closest('.input-wrap-contact');
    label = label && (label.querySelector('.input-label') ||
      (label.parentNode && label.parentNode.querySelector(':scope > .input-label')));
    if (label) trigger.setAttribute('aria-label', label.textContent.trim());

    var list = document.createElement('ul');
    list.className = 'itiz-select-list';
    list.id = id + '-list';
    list.setAttribute('role', 'listbox');
    list.tabIndex = -1;

    var activeIndex = -1;
    var typed = '';
    var typedTimer = null;

    function options() {
      return Array.prototype.slice.call(select.options);
    }

    function render() {
      list.innerHTML = '';
      options().forEach(function (opt, i) {
        if (opt.value === '' ) return; // placeholder option is shown only on the trigger
        var li = document.createElement('li');
        li.className = 'itiz-select-option';
        li.id = id + '-opt-' + i;
        li.setAttribute('role', 'option');
        li.dataset.index = i;
        li.textContent = opt.textContent;
        if (opt.disabled) li.setAttribute('aria-disabled', 'true');
        li.addEventListener('mousedown', function (e) { e.preventDefault(); });
        li.addEventListener('click', function () { choose(i); });
        li.addEventListener('mousemove', function () { setActive(i); });
        list.appendChild(li);
      });
      sync();
    }

    function items() {
      return Array.prototype.slice.call(list.children);
    }

    function sync() {
      var sel = select.options[select.selectedIndex];
      var isPlaceholder = !sel || sel.value === '';
      trigger.textContent = sel ? sel.textContent : '';
      trigger.classList.toggle('is-placeholder', isPlaceholder);
      items().forEach(function (li) {
        li.setAttribute('aria-selected', String(+li.dataset.index === select.selectedIndex));
      });
    }

    function setActive(i) {
      activeIndex = i;
      items().forEach(function (li) {
        var on = +li.dataset.index === i;
        li.classList.toggle('is-active', on);
        if (on) {
          trigger.setAttribute('aria-activedescendant', li.id);
          var top = li.offsetTop, bottom = top + li.offsetHeight;
          if (top < list.scrollTop) list.scrollTop = top;
          else if (bottom > list.scrollTop + list.clientHeight) list.scrollTop = bottom - list.clientHeight;
        }
      });
    }

    function enabledIndexes() {
      return items().filter(function (li) { return !li.hasAttribute('aria-disabled'); })
        .map(function (li) { return +li.dataset.index; });
    }

    function move(step) {
      var idx = enabledIndexes();
      if (!idx.length) return;
      var pos = idx.indexOf(activeIndex);
      if (pos === -1) pos = step > 0 ? -1 : idx.length;
      pos = Math.max(0, Math.min(idx.length - 1, pos + step));
      setActive(idx[pos]);
    }

    function open() {
      if (openInstance && openInstance !== api) openInstance.close();
      openInstance = api;
      wrap.classList.add('itiz-select-open');
      trigger.setAttribute('aria-expanded', 'true');
      var rect = trigger.getBoundingClientRect();
      var spaceBelow = window.innerHeight - rect.bottom;
      wrap.classList.toggle('itiz-select-up', spaceBelow < 260 && rect.top > spaceBelow);
      var idx = enabledIndexes();
      setActive(select.selectedIndex > 0 && idx.indexOf(select.selectedIndex) !== -1 ? select.selectedIndex : idx[0]);
    }

    function close() {
      if (openInstance === api) openInstance = null;
      wrap.classList.remove('itiz-select-open', 'itiz-select-up');
      trigger.setAttribute('aria-expanded', 'false');
      trigger.removeAttribute('aria-activedescendant');
    }

    function isOpen() {
      return wrap.classList.contains('itiz-select-open');
    }

    function choose(i) {
      if (select.selectedIndex !== i) {
        select.selectedIndex = i;
        select.dispatchEvent(new Event('input', { bubbles: true }));
        select.dispatchEvent(new Event('change', { bubbles: true }));
      }
      sync();
      close();
      trigger.focus();
    }

    trigger.addEventListener('click', function () {
      isOpen() ? close() : open();
    });

    trigger.addEventListener('keydown', function (e) {
      switch (e.key) {
        case 'ArrowDown':
        case 'ArrowUp':
          e.preventDefault();
          if (!isOpen()) open(); else move(e.key === 'ArrowDown' ? 1 : -1);
          break;
        case 'Home':
        case 'End':
          if (isOpen()) {
            e.preventDefault();
            var idx = enabledIndexes();
            setActive(e.key === 'Home' ? idx[0] : idx[idx.length - 1]);
          }
          break;
        case 'Enter':
        case ' ':
          e.preventDefault();
          if (isOpen() && activeIndex > -1) choose(activeIndex); else open();
          break;
        case 'Escape':
          if (isOpen()) { e.preventDefault(); close(); }
          break;
        case 'Tab':
          close();
          break;
        default:
          if (e.key.length === 1 && !e.ctrlKey && !e.metaKey && !e.altKey) {
            typed += e.key.toLowerCase();
            clearTimeout(typedTimer);
            typedTimer = setTimeout(function () { typed = ''; }, 500);
            var match = items().filter(function (li) {
              return !li.hasAttribute('aria-disabled') && li.textContent.toLowerCase().indexOf(typed) === 0;
            })[0];
            if (match) {
              if (isOpen()) setActive(+match.dataset.index); else choose(+match.dataset.index);
            }
          }
      }
    });

    // Keep the custom UI in sync if the value changes elsewhere (e.g. form reset)
    select.addEventListener('change', sync);
    if (select.form) select.form.addEventListener('reset', function () { setTimeout(sync, 0); });

    // Native validation bubble focuses the hidden select; hand focus to the trigger instead
    select.addEventListener('focus', function () { trigger.focus(); });
    select.addEventListener('invalid', function () { wrap.classList.add('itiz-select-invalid'); });
    select.addEventListener('change', function () { wrap.classList.remove('itiz-select-invalid'); });

    select.classList.add('itiz-select-native');
    select.setAttribute('tabindex', '-1');
    select.setAttribute('aria-hidden', 'true');
    select.insertAdjacentElement('afterend', trigger);
    trigger.insertAdjacentElement('afterend', list);

    var api = { close: close, wrap: wrap };
    render();
  }

  document.addEventListener('mousedown', function (e) {
    if (openInstance && !openInstance.wrap.contains(e.target)) openInstance.close();
  });
  window.addEventListener('resize', function () { if (openInstance) openInstance.close(); });

  function init() {
    Array.prototype.forEach.call(document.querySelectorAll('select.w-select'), enhance);
  }

  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', init);
  else init();
})();
