<script setup>
import { ref, watch } from 'vue'

const props = defineProps({
  lead: {
    type: Object,
    required: true,
  },
})

const emit = defineEmits(['cancel', 'update'])

const name = ref('')
const email = ref('')
const phone = ref('')
const company = ref('')
const status = ref('')
const source = ref('')

/* =========================
   MÁSCARA DE TELEFONE
========================= */

const formatPhone = (value) => {
  const numbers = String(value || '')
    .replace(/\D/g, '')
    .slice(0, 11)

  if (numbers.length <= 10) {
    return numbers
      .replace(/^(\d{2})(\d)/, '($1) $2')
      .replace(/(\d{4})(\d)/, '$1-$2')
  }

  return numbers
    .replace(/^(\d{2})(\d)/, '($1) $2')
    .replace(/(\d{5})(\d)/, '$1-$2')
}

const handlePhoneInput = (event) => {
  const numbersOnly = event.target.value.replace(/\D/g, '')
  phone.value = formatPhone(numbersOnly)
}

/* =========================
   CARREGAR LEAD
========================= */

watch(
  () => props.lead,
  (lead) => {
    if (lead) {
      name.value = lead.name
      email.value = lead.email
      phone.value = formatPhone(lead.phone)
      company.value = lead.company
      status.value = lead.status
      source.value = lead.source
    }
  },
  { immediate: true }
)

/* =========================
   CANCELAR
========================= */

const cancel = () => {
  emit('cancel')
}

/* =========================
   SALVAR
========================= */

const save = () => {
  const updatedLead = {
    name: name.value,
    email: email.value,
    phone: phone.value,
    company: company.value,
    status: status.value,
    source: source.value,
  }

  emit('update', {
    id: props.lead._id,
    data: updatedLead,
  })
}
</script>

<template>
  <div
    class="modal-overlay"
    @click.self="cancel"
  >
    <div class="modal">

      <!-- CABEÇALHO -->
      <div class="modal-header">
        <div>
          <h3>Editar Lead</h3>
          <p>Atualize os dados do contato.</p>
        </div>

        <button
          type="button"
          class="close-button"
          @click="cancel"
        >
          ×
        </button>
      </div>

      <!-- FORMULÁRIO -->
      <form @submit.prevent="save">

        <!-- NOME -->
        <div class="form-group">
          <label for="edit-name">
            Nome
          </label>

          <input
            id="edit-name"
            v-model="name"
            type="text"
            required
          />
        </div>

        <!-- E-MAIL -->
        <div class="form-group">
          <label for="edit-email">
            E-mail
          </label>

          <input
            id="edit-email"
            v-model="email"
            type="email"
            required
          />
        </div>

        <!-- TELEFONE + EMPRESA -->
        <div class="form-row">

          <div class="form-group">
            <label for="edit-phone">
              Telefone
            </label>

            <input
              id="edit-phone"
              :value="phone"
              type="text"
              inputmode="numeric"
              maxlength="15"
              required
              @input="handlePhoneInput"
            />
          </div>

          <div class="form-group">
            <label for="edit-company">
              Empresa
            </label>

            <input
              id="edit-company"
              v-model="company"
              type="text"
              required
            />
          </div>

        </div>

        <!-- STATUS + ORIGEM -->
        <div class="form-row">

          <div class="form-group">
            <label for="edit-status">
              Status
            </label>

            <select
              id="edit-status"
              v-model="status"
            >
              <option value="new">
                Novo
              </option>

              <option value="contacted">
                Contatado
              </option>

              <option value="qualified">
                Qualificado
              </option>
            </select>
          </div>

          <div class="form-group">
            <label for="edit-source">
              Origem
            </label>

            <select
              id="edit-source"
              v-model="source"
            >
              <option value="website">
                Website
              </option>

              <option value="instagram">
                Instagram
              </option>

              <option value="linkedin">
                LinkedIn
              </option>
            </select>
          </div>

        </div>

        <!-- BOTÕES -->
        <div class="modal-footer">

          <button
            type="button"
            class="cancel-button"
            @click="cancel"
          >
            Cancelar
          </button>

          <button
            type="submit"
            class="save-button"
          >
            Salvar alterações
          </button>

        </div>

      </form>
    </div>
  </div>
</template>

<style scoped>
/* =========================
   OVERLAY
========================= */

.modal-overlay {
  position: fixed;
  inset: 0;
  background: rgba(0, 0, 0, 0.7);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
  padding: 20px;
}

/* =========================
   MODAL
========================= */

.modal {
  width: 100%;
  max-width: 650px;
  background: #161b22;
  border: 1px solid #30363d;
  border-radius: 12px;
  padding: 28px;
  box-shadow: 0 20px 60px rgba(0, 0, 0, 0.55);
}

/* =========================
   CABEÇALHO
========================= */

.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 24px;
  padding-bottom: 20px;
  border-bottom: 1px solid #30363d;
}

.modal-header h3 {
  margin: 0 0 6px;
  color: #e1e2eb;
  font-size: 22px;
  font-weight: 400;
  letter-spacing: 1.5px;
  text-transform: uppercase;
}

.modal-header p {
  margin: 0;
  color: #999077;
  font-size: 13px;
}

.close-button {
  border: none;
  background: transparent;
  font-size: 26px;
  line-height: 1;
  cursor: pointer;
  color: #999077;
  transition: color 0.2s ease;
}

.close-button:hover {
  color: #ffd700;
}

/* =========================
   FORMULÁRIO
========================= */

.form-group {
  display: flex;
  flex-direction: column;
  gap: 8px;
  margin-bottom: 18px;
}

.form-group label {
  color: #d0c6ab;
  font-size: 11px;
  font-weight: 600;
  letter-spacing: 1px;
  text-transform: uppercase;
}

.form-group input,
.form-group select {
  padding: 11px 12px;
  background: #0b0e14;
  border: 1px solid #30363d;
  border-radius: 5px;
  color: #e1e2eb;
  font-size: 14px;
  box-sizing: border-box;
  outline: none;
  transition: border-color 0.2s ease;
}

.form-group input:focus,
.form-group select:focus {
  border-color: #ffd700;
}

.form-group select {
  cursor: pointer;
}

/* =========================
   LINHAS
========================= */

.form-row {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 16px;
}

/* =========================
   RODAPÉ
========================= */

.modal-footer {
  display: flex;
  justify-content: flex-end;
  gap: 12px;
  margin-top: 10px;
  padding-top: 20px;
  border-top: 1px solid #30363d;
}

/* =========================
   BOTÕES
========================= */

.cancel-button,
.save-button {
  padding: 11px 22px;
  border-radius: 999px;
  cursor: pointer;
  font-size: 12px;
  font-weight: 700;
  letter-spacing: 0.6px;
  transition:
    background 0.2s ease,
    border-color 0.2s ease,
    color 0.2s ease;
}

.cancel-button {
  background: transparent;
  border: 1px solid #30363d;
  color: #d0c6ab;
}

.cancel-button:hover {
  border-color: #ffd700;
  color: #ffd700;
}

.save-button {
  background: #ffd700;
  border: 1px solid #ffd700;
  color: #15171b;
}

.save-button:hover {
  background: #e9c400;
  border-color: #e9c400;
}

/* =========================
   RESPONSIVIDADE
========================= */

@media (max-width: 600px) {
  .form-row {
    grid-template-columns: 1fr;
    gap: 0;
  }

  .modal {
    padding: 20px;
  }
}
</style>