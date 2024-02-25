define(['material', 'cards/node', 'jquery'], function (mdc, Node) {
  class GenerativeAITextNode extends Node {
    editBody () {
      let body = ''

      body += '<div class="mdc-layout-grid__cell mdc-layout-grid__cell--span-12">'
      body += '<div class="mdc-select mdc-select--outlined" id="' + this.cardId + '_select_model" style="width: 100%">'
      body += '  <div class="mdc-select__anchor">'
      body += '    <span class="mdc-notched-outline">'
      body += '      <span class="mdc-notched-outline__leading"></span>'
      body += '      <span class="mdc-notched-outline__notch">'
      body += '        <span id="outlined-select-label" class="mdc-floating-label">Selected Model</span>'
      body += '      </span>'
      body += '      <span class="mdc-notched-outline__trailing"></span>'
      body += '    </span>'
      body += '    <span class="mdc-select__selected-text-container">'
      body += '      <span class="mdc-select__selected-text"></span>'
      body += '    </span>'
      body += '    <span class="mdc-select__dropdown-icon">'
      body += '      <svg class="mdc-select__dropdown-icon-graphic" viewBox="7 10 10 5" focusable="false">'
      body += '        <polygon class="mdc-select__dropdown-icon-inactive" stroke="none" fill-rule="evenodd" points="7 10 12 15 17 10"></polygon>'
      body += '        <polygon class="mdc-select__dropdown-icon-active" stroke="none" fill-rule="evenodd" points="7 15 12 10 17 15"></polygon>'
      body += '      </svg>'
      body += '    </span>'
      body += '  </div>'
      body += '  <div class="mdc-select__menu mdc-menu mdc-menu-surface mdc-menu-surface--fullwidth">'
      body += '    <ul class="mdc-list" role="listbox" aria-label=Selected Model" id="' + this.cardId + '_model_list">'
      //            body += '      <li class="mdc-list-item" aria-selected="false" data-value="GET" role="option">';
      //            body += '        <span class="mdc-list-item__ripple"></span>';
      //            body += '        <span class="mdc-list-item__text">GET</span>';
      //            body += '      </li>';
      body += '    </ul>'
      body += '  </div>'
      body += '</div>'
      body += '</div>'

      body += '<div class="mdc-layout-grid__cell mdc-layout-grid__cell--span-12">'
      body += '  <label class="mdc-text-field mdc-text-field--outlined mdc-text-field--textarea" id="' + this.cardId + '_prompt_field" style="width: 100%">'
      body += '    <span class="mdc-notched-outline">'
      body += '      <span class="mdc-notched-outline__leading"></span>'
      body += '      <div class="mdc-notched-outline__notch">'
      body += '        <label for="' + this.cardId + '_prompt_value" class="mdc-floating-label">Generative AI Prompt</label>'
      body += '      </div>'
      body += '      <span class="mdc-notched-outline__trailing"></span>'
      body += '    </span>'
      body += '    <span class="mdc-text-field__resizer">'
      body += '      <textarea class="mdc-text-field__input" rows="4" style="width: 100%" id="' + this.cardId + '_prompt_value"></textarea>'
      body += '    </span>'
      body += '  </label>'
      body += '</div>'
      body += '<div class="mdc-layout-grid__cell mdc-layout-grid__cell--span-12">'
      body += '  <label class="mdc-text-field mdc-text-field--outlined" id="' + this.cardId + '_key_field" style="width: 100%">'
      body += '    <span class="mdc-notched-outline">'
      body += '      <span class="mdc-notched-outline__leading"></span>'
      body += '      <div class="mdc-notched-outline__notch">'
      body += '        <label for="' + this.cardId + '_message_value" class="mdc-floating-label">Variable Name (Key)</label>'
      body += '      </div>'
      body += '      <span class="mdc-notched-outline__trailing"></span>'
      body += '    </span>'
      body += '    <input type="text" class="mdc-text-field__input" style="width: 100%" id="' + this.cardId + '_key_value" />'
      body += '  </label>'
      body += '</div>'

      body += '<div class="mdc-layout-grid__cell mdc-layout-grid__cell--span-7">'
      body += '  On success:'
      body += '</div>'
      body += '<div class="mdc-layout-grid__cell mdc-layout-grid__cell--span-5" style="padding-top: 8px; text-align: right;">'
      body += '  <button class="mdc-icon-button" id="' + this.cardId + '_next_edit">'
      body += '    <i class="material-icons mdc-icon-button__icon" aria-hidden="true">create</i>'
      body += '  </button>'
      body += '  <button class="mdc-icon-button" id="' + this.cardId + '_next_goto">'
      body += '    <i class="material-icons mdc-icon-button__icon" aria-hidden="true">navigate_next</i>'
      body += '  </button>'
      body += '</div>'

      body += '<div class="mdc-layout-grid__cell mdc-layout-grid__cell--span-7">'
      body += '  On error:'
      body += '</div>'
      body += '<div class="mdc-layout-grid__cell mdc-layout-grid__cell--span-5" style="padding-top: 8px; text-align: right;">'
      body += '  <button class="mdc-icon-button" id="' + this.cardId + '_error_edit">'
      body += '    <i class="material-icons mdc-icon-button__icon" aria-hidden="true">create</i>'
      body += '  </button>'
      body += '  <button class="mdc-icon-button" id="' + this.cardId + '_error_goto">'
      body += '    <i class="material-icons mdc-icon-button__icon" aria-hidden="true">navigate_next</i>'
      body += '  </button>'
      body += '</div>'
      body += '<div class="mdc-dialog" role="alertdialog" aria-modal="true" id="' + this.cardId + '-edit-dialog"  aria-labelledby="' + this.cardId + '-dialog-title" aria-describedby="' + this.cardId + '-dialog-content">'
      body += '  <div class="mdc-dialog__container">'
      body += '    <div class="mdc-dialog__surface">'
      body += '      <h2 class="mdc-dialog__title" id="' + this.cardId + '-dialog-title">Choose Destination</h2>'
      body += '      <div class="mdc-dialog__content" id="' + this.cardId + '-dialog-content"  style="padding: 0px;">'

      body += this.dialog.chooseDestinationMenu(this.cardId)

      body += '      </div>'
      body += '    </div>'
      body += '  </div>'
      body += '  <div class="mdc-dialog__scrim"></div>'
      body += '</div>'

      return body
    }

    viewBody () {
      return `<div class="mdc-typography--body1" style="margin: 16px;">Sends generative AI text prompt <em>${this.definition.prompt}</em> to <em>${this.definition.model_name}</em> and stores result in <em>${this.definition.key}</em></div>`
    }

    initialize () {
      super.initialize()

      const me = this

      const promptField = mdc.textField.MDCTextField.attachTo(document.getElementById(this.cardId + '_prompt_field'))

      if (this.definition.prompt !== undefined) {
        promptField.value = this.definition.prompt
      }

      $('#' + this.cardId + '_prompt_value').on('change keyup paste', function () {
        const value = $('#' + me.cardId + '_prompt_value').val()

        me.definition.prompt = value

        me.dialog.markChanged(me.id)
      })

      const keyField = mdc.textField.MDCTextField.attachTo(document.getElementById(this.cardId + '_key_field'))

      if (this.definition.key !== undefined) {
        keyField.value = this.definition.key
      }

      $('#' + this.cardId + '_key_value').on('change keyup paste', function () {
        const value = $('#' + me.cardId + '_key_value').val()

        me.definition.key = value

        me.dialog.markChanged(me.id)
      })

      me.dialog.initializeDestinationMenu(me.cardId, function (selected) {
      	if (me.targetDestination === 'next') {
	        me.definition.next_id = selected
	    } else {
	        me.definition.error_id = selected
		}	    

        me.dialog.markChanged(me.id)
        me.dialog.loadNode(me.definition)
      })

      const dialog = mdc.dialog.MDCDialog.attachTo(document.getElementById(me.cardId + '-edit-dialog'))

      $('#' + this.cardId + '_next_edit').on('click', function () {
      	me.targetDestination = 'next'
      	
        dialog.open()
      })

      $('#' + this.cardId + '_next_goto').on('click', function () {
        const destinationNodes = me.destinationNodes(me.dialog)

        for (let i = 0; i < destinationNodes.length; i++) {
          const destinationNode = destinationNodes[i]

          if (me.definition.next_id === destinationNode.id) {
            $("[data-node-id='" + destinationNode.id + "']").css('background-color', '#ffffff')
          } else {
            $("[data-node-id='" + destinationNode.id + "']").css('background-color', '#e0e0e0')
          }
        }

        const sourceNodes = me.sourceNodes(me.dialog)

        for (let i = 0; i < sourceNodes.length; i++) {
          const sourceNode = sourceNodes[i]

          if (me.definition.next_id === sourceNode.id) {
            $("[data-node-id='" + sourceNode.id + "']").css('background-color', '#ffffff')
          } else {
            $("[data-node-id='" + sourceNode.id + "']").css('background-color', '#e0e0e0')
          }
        }
      })

      $('#' + this.cardId + '_error_edit').on('click', function () {
      	me.targetDestination = 'error'
      	
        dialog.open()
      })

      $('#' + this.cardId + '_error_goto').on('click', function () {
        const destinationNodes = me.destinationNodes(me.dialog)

        for (let i = 0; i < destinationNodes.length; i++) {
          const destinationNode = destinationNodes[i]

          if (me.definition.error_id === destinationNode.id) {
            $("[data-node-id='" + destinationNode.id + "']").css('background-color', '#ffffff')
          } else {
            $("[data-node-id='" + destinationNode.id + "']").css('background-color', '#e0e0e0')
          }
        }

        const sourceNodes = me.sourceNodes(me.dialog)

        for (let i = 0; i < sourceNodes.length; i++) {
          const sourceNode = sourceNodes[i]

          if (me.definition.error_id === sourceNode.id) {
            $("[data-node-id='" + sourceNode.id + "']").css('background-color', '#ffffff')
          } else {
            $("[data-node-id='" + sourceNode.id + "']").css('background-color', '#e0e0e0')
          }
        }
      })

      $.get('/generative-ai/models.json', function (data) {
        const { compare } = Intl.Collator('en-US')

        data.sort(function (one, two) {
          return compare(one.name, two.name)
        })

        $.each(data, function (index, value) {
          let itemHtml = '<li class="mdc-list-item" aria-selected="false" data-value="' + value.id + '" role="option" data-name="' + value.name + '">'
          itemHtml += '  <span class="mdc-list-item__ripple"></span>'
          itemHtml += '  <span class="mdc-list-item__text">' + value.name + '</span>'
          itemHtml += '</li>'

          $('#' + me.cardId + '_model_list').append(itemHtml)
        })

        const modelField = mdc.select.MDCSelect.attachTo(document.getElementById(me.cardId + '_select_model'))

        modelField.listen('MDCSelect:change', () => {
          const originalId = me.definition.model_id

          me.definition.model_id = modelField.value
          me.definition.model_name = modelField.value

          if (originalId !== me.definition.model_id) {
            me.dialog.markChanged(me.id)
          }
        })

        if (me.definition.model_id !== undefined) {
          modelField.value = '' + me.definition.model_id
        }
      })
    }

    destinationNodes (dialog) {
      const nodes = super.destinationNodes(dialog)

      const id = this.definition.next_id

      for (let i = 0; i < this.dialog.definition.length; i++) {
        const item = this.dialog.definition[i]

        if (item.id === id) {
          nodes.push(Node.createCard(item, dialog))
        }
      }

      const error_id = this.definition.error_id

      for (let i = 0; i < this.dialog.definition.length; i++) {
        const item = this.dialog.definition[i]

        if (item.id === error_id) {
          nodes.push(Node.createCard(item, dialog))
        }
      }

      if (nodes.length === 0) {
        const node = this.dialog.resolveNode(id)

        if (node !== null) {
          nodes.push(node)
        }
      }

      return nodes
    }

    updateReferences (oldId, newId) {
      if (this.definition.next_id === oldId) {
        this.definition.next_id = newId
      }

      if (this.definition.error_id === oldId) {
        this.definition.error_id = newId
      }
    }

    cardType () {
      return 'Generative AI Text'
    }

    static cardName () {
      return 'Generative AI Text'
    }

    issues () {
      const issues = super.issues()

      if (this.definition.next_id === undefined) {
        issues.push([this.definition.id, 'Next node does not point to another node.', this.definition.name])
      } else if (this.definition.next_id === this.definition.id) {
        issues.push([this.definition.id, 'Next node points to self.', this.definition.name])
      } else if (this.isValidDestination(this.definition.next_id) === false) {
        issues.push([this.definition.id, 'Next node points to a non-existent node.', this.definition.name])
      }

      if (this.definition.error_id === undefined) {
        issues.push([this.definition.id, 'Error node does not point to another node.', this.definition.name])
      } else if (this.definition.error_id === this.definition.id) {
        issues.push([this.definition.id, 'Error node points to self.', this.definition.name])
      } else if (this.isValidDestination(this.definition.error_id) === false) {
        issues.push([this.definition.id, 'Error node points to a non-existent node.', this.definition.name])
      }


      if (this.definition.key === undefined || this.definition.key === undefined) {
        issues.push([this.definition.id, 'Variable key not defined.', this.definition.name])
      }

      return issues
    }

    static createCard (cardName) {
      const card = {
        name: cardName,
        context: '(Context goes here...)',
        key: 'variable_name',
        prompt: '(Enter your prompt here...)',
        type: 'simple-generative-ai-text',
        model_id: null,
        id: Node.uuidv4()
      }

      return card
    }
  }

  Node.registerCard('simple-generative-ai-text', GenerativeAITextNode)

  return GenerativeAITextNode
})
