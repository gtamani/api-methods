import random

def accordion(heading_elements):
    elements = {1:"One",2:"Two",3:"Three",4:"Four",5:"Five",6:"Six",
                7:"Seven",8:"Eight",9:"Nine",10:"Ten",11:"Eleven",12:"Twelve",}
    n_elements = len(heading_elements)

    result = '<div class="accordion accordion-flush" id="accordionFlushExample">'

    for element in range(1,n_elements+1):
        tail = elements[element]
        tail += [random.choice(list("abcdefghijklmnopqrstuvwxyz")) for times in range(4)][:]
        
        accordion_item = f"""
        <div class="accordion-item">
            <h2 class="accordion-header" id="flush-heading{tail}">
                <button class="accordion-button collapsed" type="button" data-bs-toggle="collapse" data-bs-target="#flush-collapse{tail}" aria-expanded="false" aria-controls="flush-collapse{tail}">
                   {heading_elements[element-1]}
                </button>
            </h2>
            <div id="flush-collapse{tail}" class="accordion-collapse collapse" aria-labelledby="flush-heading{tail}" data-bs-parent="#accordionFlushExample">


                <div class="accordion-body">


                <!--{heading_elements[element-1]} content-->
                

                </div>
            
            
            </div>
        </div>
        """
        result += accordion_item
    return result + "\n</div>"

def table():
    pass


