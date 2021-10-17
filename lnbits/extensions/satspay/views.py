from fastapi.param_functions import Depends
from starlette.exceptions import HTTPException
from starlette.responses import HTMLResponse
from starlette.requests import Request
from lnbits.core.models import User
from lnbits.core.crud import get_wallet
from lnbits.decorators import check_user_exists
from http import HTTPStatus

from fastapi.templating import Jinja2Templates

from . import satspay_ext, satspay_renderer
from .crud import get_charge

templates = Jinja2Templates(directory="templates")


@satspay_ext.get("/", response_class=HTMLResponse)
async def index(request: Request, user: User = Depends(check_user_exists)):
    return satspay_renderer().TemplateResponse(
        "satspay/index.html", {"request": request, "user": user.dict()}
    )


@satspay_ext.get("/{charge_id}", response_class=HTMLResponse)
async def display(request: Request, charge_id):
    charge = await get_charge(charge_id)
    if not charge:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail="Charge link does not exist."
        )
    return satspay_renderer().TemplateResponse(
        "satspay/display.html", {"request": request, "charge": charge}
    )
