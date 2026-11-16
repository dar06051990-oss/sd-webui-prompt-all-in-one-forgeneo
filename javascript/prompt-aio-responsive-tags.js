// Prompt All-in-One / Forge Neo — responsive tag layout safeguard (v1.1.10 TEST).
// Loaded automatically by Forge's standard extensions/javascript loader.
// The original Prompt AIO front-end measures the tag only once, then writes
// pixel heights inline on the edit row and the delete button. When translated
// strings / window zoom change wrapping, these stale heights cause overlap.
// Restore content-driven row height and reserve real space for the delete icon.
(() => {
    const styleId = 'prompt-aio-responsive-tag-layout-v1110';
    if (document.getElementById(styleId)) return;
    const style = document.createElement('style');
    style.id = styleId;
    style.textContent = `
/* Only Prompt AIO's tag list; not Forge's native prompt or other extensions. */
.physton-prompt .prompt-tags .prompt-tags-list .prompt-tag {
  box-sizing: border-box;
  min-width: 0;
  max-width: 100%;
}
.physton-prompt .prompt-tags .prompt-tags-list .prompt-tag .prompt-tag-main {
  min-width: 0;
  max-width: 100%;
  height: auto !important;
}
.physton-prompt .prompt-tags .prompt-tags-list .prompt-tag .prompt-tag-main .prompt-tag-edit {
  box-sizing: border-box;
  min-width: 0;
  max-width: 100%;
  height: auto !important; /* cancel stale JS px height after zoom/text update */
  align-items: stretch !important;
}
.physton-prompt .prompt-tags .prompt-tags-list .prompt-tag .prompt-tag-main .prompt-tag-edit .prompt-tag-value {
  box-sizing: border-box;
  flex: 1 1 auto;
  min-width: 0;
  max-width: 100%;
  width: auto !important;
  height: auto !important;
  overflow-wrap: anywhere;
}
.physton-prompt .prompt-tags .prompt-tags-list .prompt-tag .prompt-tag-main .prompt-tag-edit .prompt-tag-value .character {
  max-width: 100%;
  min-width: 0;
  overflow-wrap: anywhere;
}
.physton-prompt .prompt-tags .prompt-tags-list .prompt-tag .prompt-tag-main .prompt-tag-edit .btn-tag-delete {
  box-sizing: border-box;
  flex: 0 0 16px !important;
  width: 16px !important;
  min-width: 16px !important;
  height: auto !important;
  min-height: 26px;
  align-self: stretch !important;
}
.physton-prompt .prompt-tags .prompt-tags-list .prompt-tag .prompt-tag-main .prompt-tag-edit .input-tag-edit {
  box-sizing: border-box;
  flex: 1 1 auto;
  min-width: 0;
}
.physton-prompt .prompt-tags .prompt-tags-list .prompt-tag .prompt-local-language {
  min-width: 0;
  max-width: 100%;
}
.physton-prompt .prompt-tags .prompt-tags-list .prompt-tag .prompt-local-language .local-language {
  min-width: 0;
  overflow-wrap: anywhere;
  white-space: normal;
}
`;
    (document.head || document.documentElement).appendChild(style);
})();
