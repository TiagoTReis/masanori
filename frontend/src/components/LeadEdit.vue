
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
   MODAL
========================= */

.modal-overlay {
  position: fixed;
  inset: 0;
  background: rgba(0, 0, 0, 0.65);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
  padding: 20px;
}

.modal {
  width: 100%;
  max-width: 650px;
  background: #ffffff;
  border-radius: 12px;
  padding: 28px;
  box-shadow: 0 20px 60px rgba(0, 0, 0, 0.35);
}

/* =========================
   CABEÇALHO
========================= */

.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 24px;
}

.modal-header h3 {
  margin: 0 0 6px;
  font-size: 24px;
}

.modal-header p {
  margin: 0;
  color: #666;
}

.close-button {
  border: none;
  background: transparent;
  font-size: 28px;
  cursor: pointer;
  color: #666;
}

/* =========================
   FORMULÁRIO
========================= */

.form-group {
  display: flex;
  flex-direction: column;
  gap: 6px;
  margin-bottom: 18px;
}

.form-group label {
  font-weight: 600;
}

.form-group input,
.form-group select {
  padding: 10px 12px;
  border: 1px solid #ccc;
  border-radius: 6px;
  font-size: 15px;
  box-sizing: border-box;
}

.form-group input:focus,
.form-group select:focus {
  outline: none;
  border-color: #1d4ed8;
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
}

/* =========================
   BOTÕES
========================= */

.cancel-button,
.save-button {
  padding: 10px 18px;
  border-radius: 6px;
  cursor: pointer;
  font-size: 14px;
}

.cancel-button {
  background: #fff;
  border: 1px solid #ccc;
}

.cancel-button:hover {
  background: #f5f5f5;
}

.save-button {
  background: #1d4ed8;
  border: 1px solid #1d4ed8;
  color: #fff;
}

.save-button:hover {
  background: #1e40af;
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
